from django.conf import settings
from django.db import models


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
    bio = models.TextField(
        max_length=500,
        blank=True,
    )

    @property
    def is_complete(self):
        return bool(self.display_name and self.display_name.strip())

    def __str__(self):
        return self.display_name
