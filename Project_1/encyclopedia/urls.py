from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),   
    path("<str:name>", views.entry, name="entry"),
    path("get_result/", views.get_result, name="get_result"),
    path("new_result/", views.new_result, name="new_result"),
    path("save_result/", views.save_result, name="save_result"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("edit_result/", views.edit_result, name="edit_result"),    
    path("random_result/", views.random_result, name="random_result")
]
