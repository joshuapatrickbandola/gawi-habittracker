from django.urls import path

from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("accounts/profile/setup/<int:step>/", set_profile, name="set_profile"),
    path("accounts/profile/post-login/", post_login, name="post_login"),
    path("accounts/profile/post-signup/", post_signup, name="post_signup"),
    path("accounts/profile/<username>/", profile_view, name="profile_view"),
    path("accounts/profile/update", profile_edit, name="profile_edit"),
    path("push/subscribe/", PushSubscribeView.as_view(), name="push_subscribe"),
]

app_name = "accounts"
