from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import BioForm, DisplayNameForm, ProfilePictureForm

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
def update_profile(request):
    return render(request, "profile_update.html")


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
