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
    path("editEvent/<str:event_id>", views.editEvent, name="editEvent"),
    path("deleteEvent/<str:event_id>", views.deleteEvent, name="deleteEvent"),

    path("userFeed/", views.feed, name="userFeed"),
]
