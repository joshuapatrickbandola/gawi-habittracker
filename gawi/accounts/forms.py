from allauth.account.forms import (
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SignupForm,
)
from django import forms

from .models import Profile


class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["login"].widget.attrs.update(
            {
                "class": "input",
            }
        )

        self.fields["password"].widget.attrs.update(
            {
                "class": "input",
            }
        )


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {
                "class": "input",
            }
        )

        self.fields["password1"].widget.attrs.update(
            {
                "class": "input",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "input",
            }
        )


class CustomResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update(
            {
                "class": "input",
            }
        )


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update(
            {
                "class": "input",
            }
        )

        self.fields["password2"].widget.attrs.update(
            {
                "class": "input",
            }
        )


class DisplayNameForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name"]  # noqa: RUF012


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_picture"]  # noqa: RUF012


class BioForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio"]  # noqa: RUF012
