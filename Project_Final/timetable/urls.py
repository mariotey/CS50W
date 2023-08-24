from django.urls import path
from . import views

app_name = "timetable"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path("mainTable/", views.index, name="mainTable"),
    path("createEvent/", views.createEvent, name="createEvent"),
]

