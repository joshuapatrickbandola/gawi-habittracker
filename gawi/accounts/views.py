from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max, Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from habittracker.models import HabitAccomplishment, HabitStreak

from .forms import BioForm, DisplayNameForm, ProfileEditForm, ProfilePictureForm

User = get_user_model()

FORMS = {
    1: DisplayNameForm,
    2: ProfilePictureForm,
    3: BioForm,
}


def home(request):
    return render(request, "home.html")


@login_required
def set_profile(request, step):
    if step not in FORMS:
        raise Http404("Invalid setup step.")
    profile = request.user.profile

    previous_step = step - 1

    form_class = FORMS[step]

    if request.method == "POST":
        form = form_class(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()

            if step < 3:
                return redirect("accounts:set_profile", step=step + 1)

            return redirect(
                "habittracker:dashboard",
                username=request.user.username,
            )

    else:
        form = form_class(instance=profile)

    return render(
        request,
        "profile_setup.html",
        {
            "form": form,
            "step": step,
            "previous_step": previous_step,
        },
    )


@login_required
def profile_edit(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("accounts:profile_view", request.user.username)
    else:
        form = ProfileEditForm(instance=profile)

    return render(
        request,
        "profile_update.html",
        {
            "form": form,
            "profile": profile,
        },
    )


@login_required
def post_login(request):
    profile = request.user.profile

    if not profile.display_name:
        return redirect("accounts:set_profile", step=1)

    return redirect(
        "habittracker:dashboard",
        username=request.user.username,
    )


@login_required
def post_signup(request):
    profile = request.user.profile

    if profile.display_name:
        return redirect(
            "habittracker:dashboard",
            username=request.user.username,
        )

    return redirect("accounts:set_profile", step=1)


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    habits = profile_user.profile.habits.filter(is_archived=False)

    streak_stats = HabitStreak.objects.filter(
        habit__in=habits,
        archived_at__isnull=True,
    ).aggregate(
        current_streak=Max("current_streak"),
        longest_streak=Max("longest_streak"),
    )

    accomplishment_stats = HabitAccomplishment.objects.filter(
        habit__in=habits,
    ).aggregate(
        total=Count("id"),
        completed=Count("id", filter=Q(completed=True)),
    )

    total = accomplishment_stats["total"] or 0
    completed = accomplishment_stats["completed"] or 0
    completion_rate = round((completed / total) * 100) if total else 0

    context = {
        "profile_user": profile_user,
        "current_streak": streak_stats["current_streak"] or 0,
        "longest_streak": streak_stats["longest_streak"] or 0,
        "habit_count": habits.count(),
        "completion_rate": completion_rate,
    }
    return render(request, "profile_view.html", context)


import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from .models import PushSubscription


class PushSubscribeView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            endpoint = data["endpoint"]
            keys = data["keys"]
            p256dh = keys["p256dh"]
            auth = keys["auth"]
        except (json.JSONDecodeError, KeyError, TypeError):
            return JsonResponse({"error": "Invalid subscription payload."}, status=400)

        PushSubscription.objects.update_or_create(
            profile=request.user.profile,
            endpoint=endpoint,
            defaults={"p256dh": p256dh, "auth": auth},
        )
        return JsonResponse({"status": "subscribed"})
