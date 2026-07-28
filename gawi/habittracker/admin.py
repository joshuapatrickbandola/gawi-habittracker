from django.contrib import admin

from .models import (
    Achievement,
    Category,
    Habit,
    HabitAccomplishment,
    HabitStreak,
    UserAchievement,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "profile",
        "category",
        "notification_interval",
        "is_archived",
        "created_at",
    )
    list_filter = (
        "is_archived",
        "category",
        "created_at",
    )
    search_fields = (
        "name",
        "goal",
        "profile__user__username",
    )
    autocomplete_fields = (
        "profile",
        "category",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("-created_at",)


@admin.register(HabitStreak)
class HabitStreakAdmin(admin.ModelAdmin):
    list_display = (
        "habit",
        "current_streak",
        "longest_streak",
    )
    search_fields = (
        "habit__name",
        "habit__profile__user__username",
    )
    autocomplete_fields = ("habit",)


@admin.register(HabitAccomplishment)
class HabitAccomplishmentAdmin(admin.ModelAdmin):
    list_display = (
        "habit",
        "date",
        "completed",
    )
    list_filter = (
        "completed",
        "date",
    )
    search_fields = (
        "habit__name",
        "habit__profile__user__username",
    )
    autocomplete_fields = ("habit",)
    ordering = ("-date",)


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "type",
        "requirement",
    )
    list_filter = ("type",)
    search_fields = (
        "name",
        "description",
    )
    ordering = ("type", "requirement")


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = (
        "profile",
        "achievement",
        "earned_at",
    )
    list_filter = (
        "achievement",
        "earned_at",
    )
    search_fields = (
        "profile__user__username",
        "achievement__name",
    )
    autocomplete_fields = (
        "profile",
        "achievement",
    )
    ordering = ("-earned_at",)
