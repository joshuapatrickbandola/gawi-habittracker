from django.urls import path

from . import views

app_name = "habittracker"

urlpatterns = [
    path("<username>/dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("<username>/habits/", views.HabitListView.as_view(), name="habit_list"),
    path("<username>/habit/add/", views.HabitCreateView.as_view(), name="habit_create"),
    path(
        "<str:username>/<int:pk>/edit/",
        views.HabitUpdateView.as_view(),
        name="habit_edit",
    ),
    path(
        "habit/<int:pk>/complete/",
        views.HabitCompleteView.as_view(),
        name="habit_complete",
    ),
    path(
        "habits/<int:pk>/delete/",
        views.HabitDeleteView.as_view(),
        name="habit_delete",
    ),
    path(
        "tasks/send-due-notifications/",
        views.trigger_due_notifications,
        name="send_due_notifications",
    ),
]
