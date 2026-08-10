import datetime
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max, Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import (
    Achievement,
    Habit,
    HabitAccomplishment,
    HabitStreak,
    UserAchievement,
)

HEATMAP_WEEKS = 53


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        user = self.request.user

        profile = user.profile

        habits = Habit.objects.filter(
            profile=profile,
            is_archived=False,
        )

        context.update(
            {
                "habits": habits,
                "habit_count": habits.count(),
                "today_habits": self.get_today_habits(habits),
                "profile_streak": self.calculate_profile_streak(habits),
                "achievement_progress": self.get_achievement_progress(profile),
                "weekly_report": self.get_weekly_report(habits),
                "heatmap": self.get_heatmap(habits),
                "struggling_habits": self.get_missed_habits(habits),
            }
        )

        return context

    def get_today_habits(self, habits):
        """
        Returns the all the habits and their
        respective names, status, and streak.
        """

        today = timezone.localtime(timezone.now()).date()

        data = []

        for habit in habits:
            completed = habit.accomplishments.filter(
                date=today, completed=True
            ).exists()

            data.append(
                {
                    "habit": habit,
                    "completed": completed,
                    "streak": habit.streak.current_streak,
                }
            )

        return data

    def calculate_profile_streak(self, habits):
        """
        Counts consecutive days where at least
        one habit was completed.
        """

        dates = set(
            HabitAccomplishment.objects.filter(
                habit__in=habits, completed=True
            ).values_list("date", flat=True)
        )

        streak = 0

        day = timezone.now().date()

        while day in dates:
            streak += 1

            day -= timedelta(days=1)

        return streak

    def get_achievement_progress(self, profile):
        all_achievements = Achievement.objects.order_by("requirement")

        earned_ids = set(profile.achievements.values_list("achievement_id", flat=True))

        next_achievement = None

        for achievement in all_achievements:
            if achievement.id not in earned_ids:
                next_achievement = achievement
                break

        earned_achievements = all_achievements.filter(id__in=earned_ids)

        return {
            "earned": earned_achievements,
            "next": next_achievement,
            "all": all_achievements,
        }

    def get_weekly_report(self, habits):

        today = date.today()  # noqa: DTZ011
        start_week = today - timedelta(days=(today.weekday() + 1) % 7)

        data = []

        for i in range(7):
            current_day = start_week + timedelta(days=i)

            completed = HabitAccomplishment.objects.filter(
                habit__in=habits,
                date=current_day,
                completed=True,
            ).count()

            data.append(
                {
                    "day": current_day.strftime("%A"),
                    "completed": completed,
                }
            )

        return data

    def get_heatmap(self, habits):

        today = date.today()  # noqa: DTZ011

        quarter = (today.month - 1) // 3
        start_month = quarter * 3 + 1

        quarter_names = ["JAN-MAR", "APR-JUN", "JUL-SEP", "OCT-DEC"]

        start_date = date(today.year, start_month, 1)

        if start_month == 10:
            end_date = date(today.year + 1, 1, 1)
        else:
            end_date = date(today.year, start_month + 3, 1)

        data = []

        start_offset = (start_date.weekday() + 1) % 7

        for _ in range(start_offset):
            data.append(
                {
                    "date": None,
                    "count": None,
                    "placeholder": True,
                }
            )

        current_day = start_date

        while current_day < end_date:
            if current_day > today:
                count = None
            else:
                count = HabitAccomplishment.objects.filter(
                    habit__in=habits,
                    date=current_day,
                    completed=True,
                ).count()

                if count == 0:
                    level = 0
                elif count <= 1:
                    level = 1
                elif count <= 3:
                    level = 2
                elif count <= 5:
                    level = 3
                else:
                    level = 4

            data.append(
                {
                    "date": current_day,
                    "count": count,
                    "level": level,
                    "placeholder": False,
                }
            )

            current_day += timedelta(days=1)

        remainder = len(data) % 7

        if remainder:
            for _ in range(7 - remainder):
                data.append(
                    {
                        "date": None,
                        "count": None,
                        "placeholder": True,
                    }
                )

        return {
            "quarter": quarter_names[quarter],
            "year": today.year,
            "data": data,
        }

    def get_missed_habits(self, habits):
        result = []

        for habit in habits:
            records = list(
                HabitAccomplishment.objects.filter(habit=habit).order_by("-date")
            )

            if not records or records[0].completed:
                continue

            missed = 0
            for record in records:
                if not record.completed:
                    missed += 1
                else:
                    break

            if missed > 0:
                result.append({"habit": habit, "missed": missed})

        return sorted(result, key=lambda x: x["missed"], reverse=True)


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    template_name = "habit_list.html"
    context_object_name = "habits"

    def get_queryset(self):
        today = timezone.localtime(timezone.now()).date()
        heatmap_start = self._heatmap_start_date(today)

        return (
            Habit.objects.filter(
                profile=self.request.user.profile,
                is_archived=False,
            )
            .select_related("category", "streak")
            .prefetch_related(
                Prefetch(
                    "accomplishments",
                    queryset=HabitAccomplishment.objects.filter(date=today),
                    to_attr="today_completion",
                ),
                Prefetch(
                    "accomplishments",
                    queryset=HabitAccomplishment.objects.filter(
                        date__gte=heatmap_start,
                        date__lte=today,
                        completed=True,
                    ),
                    to_attr="heatmap_accomplishments",
                ),
            )
        )

    @staticmethod
    def _heatmap_start_date(today):
        start = today - datetime.timedelta(weeks=HEATMAP_WEEKS - 1)
        days_since_sunday = (start.weekday() + 1) % 7
        return start - datetime.timedelta(days=days_since_sunday)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localtime(timezone.now()).date()
        heatmap_start = self._heatmap_start_date(today)

        for habit in context["habits"]:
            habit.heatmap_weeks = self._build_heatmap(
                habit.heatmap_accomplishments, heatmap_start, today
            )
        return context

    @staticmethod
    def _build_heatmap(accomplishments, start_date, end_date):
        completed_dates = {a.date for a in accomplishments}

        weeks, week = [], []
        current = start_date
        while current <= end_date:
            week.append({"date": current, "completed": current in completed_dates})
            if current.weekday() == 5:
                weeks.append(week)
                week = []
            current += datetime.timedelta(days=1)

        if week:
            while len(week) < 7:
                week.append({"date": None, "completed": False})
            weeks.append(week)

        return weeks


class HabitCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        habit = get_object_or_404(Habit, pk=pk, profile=request.user.profile)
        today = timezone.localtime(timezone.now()).date()

        accomplishment, _ = HabitAccomplishment.objects.get_or_create(
            habit=habit,
            date=today,
        )
        accomplishment.completed = not accomplishment.completed
        accomplishment.save()

        habit.streak.recalculate()

        if accomplishment.completed:
            self._check_achievements(request.user.profile)

        return JsonResponse({"completed": accomplishment.completed})

    def _check_achievements(self, profile):
        best_streak = (
            HabitStreak.objects.filter(habit__profile=profile)
            .aggregate(best=Max("longest_streak"))
            .get("best")
            or 0
        )

        eligible = Achievement.objects.filter(requirement__lte=best_streak).exclude(
            id__in=profile.achievements.values_list("achievement_id", flat=True)
        )

        for achievement in eligible:
            UserAchievement.objects.get_or_create(
                profile=profile,
                achievement=achievement,
            )


class HabitFormStylingMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields["name"].widget.attrs.update(
            {"class": "habit-name-field", "placeholder": "Habit Name"}
        )
        form.fields["category"].widget.attrs.update({"class": "habit-category-field"})
        form.fields["category"].empty_label = "Category"
        form.fields["goal"].widget.attrs.update(
            {
                "class": "habit-goal-field",
                "placeholder": "What is your goal by end of the year?",
            }
        )
        form.fields["color"].widget.attrs.update({"class": "habit-color-field"})
        form.fields["notification_interval"].widget.attrs.update(
            {"class": "habit-notification"}
        )

        return form


class HabitCreateView(HabitFormStylingMixin, LoginRequiredMixin, CreateView):
    model = Habit
    template_name = "habit_form.html"

    fields = [  # noqa: RUF012
        "name",
        "category",
        "goal",
        "color",
        "notification_interval",
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vapid_public_key"] = settings.VAPID_PUBLIC_KEY
        return context

    def get_success_url(self):
        return reverse_lazy(
            "habittracker:habit_list",
            kwargs={"username": self.request.user.username},
        )

    def form_valid(self, form):

        profile = self.request.user.profile

        form.instance.profile = profile

        custom_category = self.request.POST.get("custom_category", "").strip()

        if custom_category:
            form.instance.category = None
            form.instance.custom_category = custom_category

        response = super().form_valid(form)

        HabitStreak.objects.create(
            habit=self.object,
            current_streak=0,
            longest_streak=0,
        )

        return response


class HabitUpdateView(
    HabitFormStylingMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    model = Habit
    template_name = "habit_form.html"
    fields = [  # noqa: RUF012
        "name",
        "category",
        "goal",
        "color",
        "notification_interval",
    ]

    def test_func(self):
        habit = self.get_object()
        return habit.profile == self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["vapid_public_key"] = settings.VAPID_PUBLIC_KEY
        return context

    def get_success_url(self):
        return reverse_lazy(
            "habittracker:habit_list", kwargs={"username": self.request.user.username}
        )

    def form_valid(self, form):
        custom_category = self.request.POST.get("custom_category", "").strip()
        if custom_category:
            form.instance.category = None
            form.instance.custom_category = custom_category
        else:
            form.instance.custom_category = ""

        return super().form_valid(form)


class HabitDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Habit

    def test_func(self):
        habit = self.get_object()
        return habit.profile == self.request.user.profile

    def get_success_url(self):
        return reverse(
            "habittracker:habit_list",
            kwargs={"username": self.request.user.username},
        )

    def post(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
