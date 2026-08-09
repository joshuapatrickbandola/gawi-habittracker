from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
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


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        profile = user.profile

        picture = sociallogin.account.extra_data.get("picture")
        if picture and not profile.google_picture:
            profile.google_picture = picture
            profile.save()

        return user
