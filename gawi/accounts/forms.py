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


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [  # noqa: RUF012
            "display_name",
            "profile_picture",
            "bio",
        ]
        widgets = {  # noqa: RUF012
            "display_name": forms.TextInput(
                attrs={
                    "placeholder": "Enter your display name",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Tell us a little about yourself (optional)",
                }
            ),
        }

    def clean_display_name(self):
        display_name = self.cleaned_data["display_name"].strip()

        if not display_name:
            raise forms.ValidationError("Display name is required.")

        return display_name
