from django.urls import path

from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("accounts/profile/set", set_profile, name="set_profile"),
    path("accounts/profile/update", update_profile, name="update_profile"),
]

app_name = "accounts"
