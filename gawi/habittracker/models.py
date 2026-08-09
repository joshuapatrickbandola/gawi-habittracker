from datetime import timedelta

from accounts.models import Profile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class meta:
        verbose_name = "category"
        verbose_name_plural = "categories"


class Habit(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="habits",
    )
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="habits",
    )
    color = models.CharField(
        max_length=7,
        default="#36E91F",
        help_text="Hex color code (e.g. #36E91F)",
    )
    goal = models.TextField(blank=True)
    notification_interval = models.IntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(24),
        ],
        help_text="Notify the user every X hours (1-24).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class HabitStreak(models.Model):
    habit = models.OneToOneField(
        Habit,
        on_delete=models.CASCADE,
        related_name="streak",
    )
    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)

    archived_at = models.DateTimeField(null=True, blank=True)

    def recalculate(self):
        today = timezone.now().date()
        streak = 0
        day = today

        while self.habit.accomplishments.filter(
            date=day,
            completed=True,
        ).exists():
            streak += 1
            day -= timedelta(days=1)

        self.current_streak = streak
        self.longest_streak = max(self.longest_streak, streak)
        self.save()

    def __str__(self):
        return f"{self.habit.name} Streak"


class HabitAccomplishment(models.Model):
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name="accomplishments",
    )
    date = models.DateField()
    completed = models.BooleanField(default=False)

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["habit", "date"],
                name="unique_habit_accomplishment_per_day",
            )
        ]
        indexes = [  # noqa: RUF012
            models.Index(fields=["date"]),
        ]
        ordering = ["-date"]  # noqa: RUF012

    def __str__(self):
        return f"{self.habit.name} - {self.date}"


class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    requirement = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="achievements",
    )
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name="users",
    )
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [  # noqa: RUF012
            models.UniqueConstraint(
                fields=["profile", "achievement"],
                name="unique_user_achievement",
            )
        ]

    def __str__(self):
        return f"{self.profile} - {self.achievement.name}"
