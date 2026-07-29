from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import *

FORMS = {
    1: DisplayNameForm,
    2: ProfilePictureForm,
    3: BioForm,
}


def home(request):
    return render(request, "home.html")


def set_profile(request, step):
    profile = request.user.profile

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
        },
    )


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

    if profile.is_complete:
        return redirect(
            "habittracker:dashboard",
            username=request.user.username,
        )

    return redirect("accounts:set_profile", step=1)
