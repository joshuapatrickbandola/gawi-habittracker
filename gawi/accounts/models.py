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


class PushSubscription(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="push_subscriptions",
    )
    endpoint = models.URLField(max_length=500, unique=True)
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["profile", "endpoint"], name="unique_profile_endpoint"
            ),
        ]

    def __str__(self):
        return f"{self.profile} push subscription"
