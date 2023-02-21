from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),   
    path("<str:name>", views.entry, name="entry"),
    path("get_result/", views.get_result, name="get_result")
]
