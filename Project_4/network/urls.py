
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("submit", views.submitpost, name="submitpost"),

    path("<str:name>", views.user_profile, name="user_profile"),
    path("follow/<str:name>", views.follow_user, name="follow_user"),
]

