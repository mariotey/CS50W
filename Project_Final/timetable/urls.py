from django.urls import path
from . import views

app_name = "timetable"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("mainTable/", views.mainTable, name="mainTable"),
    path("newEvent/", views.newEvent, name="newEvent"),
    path("existEvent/", views.existEvent, name="existEvent"),
    path("createEvent/", views.createEvent, name="createEvent"),
]
