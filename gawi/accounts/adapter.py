from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse


class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        profile = request.user.profile

        if not profile.display_name:
            return reverse("accounts:set_profile")

        return reverse(
            "habittracker:dashboard",
            kwargs={"username": request.user.username},
        )
