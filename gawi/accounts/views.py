from django.shortcuts import redirect, render

from .forms import ProfileSetupForm


def home(request):
    return render(request, "home.html")


def set_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileSetupForm(
            request.POST,
            request.FILES,
            instance=profile,
        )

        if form.is_valid():
            form.save()
            return redirect("accounts:home")
    else:
        form = ProfileSetupForm(instance=profile)

    ctx = {
        "form": form,
    }
    return render(request, "profile_setup.html", ctx)


def update_profile(request):
    return render(request, "profile_update.html")
