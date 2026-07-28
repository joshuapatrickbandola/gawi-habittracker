from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    ListView,
    TemplateView,
    UpdateView,
)

from .models import (
    Habit,
    HabitAccomplishment,
    HabitStreak,
    UserAchievement,
)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.kwargs["username"]

        user = User.objects.get(username=username)

        habits = Habit.objects.filter(profile__user=user)

        # Calendar heatmap data
        accomplishments = HabitAccomplishment.objects.filter(
            habit__in=habits,
            completed=True,
        )

        # Achievements
        achievements = UserAchievement.objects.filter(profile__user=user)

        # Current daily profile streak
        daily_streak = self.calculate_daily_streak(accomplishments)

        # Weekly report data
        weekly_data = self.get_weekly_report(habits)

        context.update(
            {
                "habits": habits,
                "accomplishments": accomplishments,
                "achievements": achievements,
                "daily_streak": daily_streak,
                "weekly_data": weekly_data,
            }
        )

        return context

    def calculate_daily_streak(self, accomplishments):
        """
        Counts consecutive days where at least
        one habit was completed.
        """

        dates = set(accomplishments.values_list("date", flat=True))

        streak = 0
        today = __import__("datetime").date.today()

        while today in dates:
            streak += 1
            today -= __import__("datetime").timedelta(days=1)

        return streak

    def get_weekly_report(self, habits):
        """
        Generates weekly completion statistics.
        """

        from datetime import date, timedelta

        today = date.today()  # noqa: DTZ011
        start_week = today - timedelta(days=today.weekday())

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


class HabitListView(LoginRequiredMixin, ListView):
    model = Habit
    template_name = "habit_list.html"
    context_object_name = "habits"

    def get_queryset(self):
        today = timezone.now().date()

        return (
            Habit.objects.filter(
                profile=self.request.user.profile,
                is_archived=False,
            )
            .select_related(
                "category",
                "streak",
            )
            .prefetch_related(
                Prefetch(
                    "accomplishments",
                    queryset=HabitAccomplishment.objects.filter(date=today),
                    to_attr="today_completion",
                )
            )
        )


class HabitCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):

        habit = get_object_or_404(Habit, pk=pk, profile=request.user.profile)

        today = timezone.now().date()

        accomplishment, _ = HabitAccomplishment.objects.get_or_create(
            habit=habit,
            date=today,
        )

        accomplishment.completed = not accomplishment.completed

        accomplishment.save()

        habit.streak.recalculate()

        return JsonResponse({"completed": accomplishment.completed})


class HabitCreateView(LoginRequiredMixin, CreateView):
    model = Habit
    template_name = "habit_form.html"

    fields = [  # noqa: RUF012
        "name",
        "category",
        "goal",
        "color",
        "notification_interval",
    ]

    def get_success_url(self):
        return reverse_lazy(
            "habittracker:habit_list",
            kwargs={"username": self.request.user.username},
        )

    def form_valid(self, form):

        profile = self.request.user.profile

        form.instance.profile = profile

        response = super().form_valid(form)

        HabitStreak.objects.create(
            habit=self.object,
            current_streak=0,
            longest_streak=0,
        )

        return response


class HabitUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Habit
    template_name = "habit_form.html"

    fields = [  # noqa: RUF012
        "name",
        "category",
        "goal",
        "color",
        "notification_interval",
    ]

    success_url = reverse_lazy("habittracker:habit-list")

    def test_func(self):

        habit = self.get_object()

        return habit.profile.user == self.request.user
