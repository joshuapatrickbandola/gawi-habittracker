from django.conf import settings
from django.db import models
from django.templatetags.static import static


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    display_name = models.CharField(max_length=63)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/",
        blank=True,
        null=True,
    )
    google_picture = models.URLField(blank=True)
    bio = models.TextField(
        max_length=500,
        blank=True,
    )

    @property
    def avatar_url(self):
        if self.profile_picture:
            return self.profile_picture.url

        if self.google_picture:
            return self.google_picture

        return static("img/default-avatar.png")

    def __str__(self):
        return self.display_name
