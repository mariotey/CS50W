""" Table of Contents of all the URL paths web application can run """
""" Tells what response to return when a particular URL is visited """

from django.urls import path
from . import views

app_name = "auctions"

urlpatterns = [
    
    # Giving a string name to a URL path makes it easier to reference it from other parts of the application 
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create_list/", views.create_list, name="create_list"),
    path("view_list/<str:name>", views.view_list, name="view_list"),
    # path("addwatchlist/<str:name>",views.addwatchlist,name="addwatchlist"),
    # path("removewatchlist/<str:name>",views.removewatchlist,name="removewatchlist"),
    path("close_auc/<str:name>", views.close_auc, name="close_auc"),
]
