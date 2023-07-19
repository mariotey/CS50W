""" Describes what users see or what the webpage renders when they visit a particular route  """

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import User, Listing, Bid
from datetime import datetime

# Default View
def index(request):      
    return render(request, "auctions/index.html", {
        "activelist_objects": Listing.objects.all(),
    })

###################################################################################################

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.watchlist = []

            user.save()

        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

################################################################################################### 
   
def create_list(request):
    if request.method == "POST":
        listing = Listing(
            title=request.POST["title"],
            description=request.POST["description"],
            category=request.POST["category"],
            image_url=request.POST["image_url"],
            start_bid=request.POST["start_bid"],
            active_stat = True,
            creator=User.objects.get(username=request.user),
            created_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        listing.save()

        return HttpResponseRedirect(reverse("auctions:index"))

    return render(request, "auctions/create_list.html")

def view_list(request, name):    
    listing = Listing.objects.get(title=name)

    return render(request, "auctions/view_list.html",{
        "view_list": listing,
    })

# def addwatchlist(request,name):
#     if request.user.username:
#         w = WatchList()
#         w.user = request.user.username
#         w.listingid = name
#         w.save()
        
#         return redirect('listingpage',HttpResponseRedirect(reverse("view_list",args=[name]), {
#             "view_list": Listing.objects.get(title=name),
#         }))
#     else:
#         return redirect('index')

# def removewatchlist(request,listingid):
#     if request.user.username:
#         try:
#             w = WatchList.objects.get(user=request.user.username,listingid=listingid)
#             w.delete()
#             return redirect('listingpage',id=listingid)
#         except:
#             return redirect('listingpage',id=listingid)
#     else:
#         return redirect('index')


def close_auc(request, name):
    listing = Listing.objects.get(title=name)

    listing.active_stat = False
    listing.save()
    
    return HttpResponseRedirect(reverse("auctions:view_list",args=[name]), {
        "view_list": listing,
    })


