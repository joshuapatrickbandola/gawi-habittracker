from django.urls import path

from . import views

app_name = "habittracker"

urlpatterns = [
    path("<username>/dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("<username>/habits/", views.HabitListView.as_view(), name="habit_list"),
    path("<username>/habit/add/", views.HabitCreateView.as_view(), name="habit_create"),
    path(
        "<username>/<habit_name>/edit/",
        views.HabitUpdateView.as_view(),
        name="habit_edit",
    ),
    path(
        "habit/<int:pk>/complete/",
        views.HabitCompleteView.as_view(),
        name="habit_complete",
    ),
]
