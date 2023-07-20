""" Table of Contents of all the URL paths web application can run """
""" Tells what response to return when a particular URL is visited """

from django.urls import path
from . import views

app_name = "auctions"

urlpatterns = [
    
    # Giving a string name to a URL path makes it easier to reference it from other parts of the application 
    
    # User Login Paths
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),

    # Listing Paths
    path("create_list/", views.create_list, name="create_list"),
    path("view_list/<str:title>", views.view_list, name="view_list"),
    path("close_auc/<str:title>", views.close_auc, name="close_auc"),

    # Biding Paths
    path("bid/<str:title>", views.bid, name="bid"),

    # Watchlist Paths
    path("watchlist/", views.view_watchlist, name="view_watchlist"),
    path("watchlist/<str:title>",views.watchlist,name="watchlist"),

]
