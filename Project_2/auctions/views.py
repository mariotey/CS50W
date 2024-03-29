""" Describes what users see or what the webpage renders when they visit a particular route  """

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import User, Listing, Bid, WatchList, Comment
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
            bid_value=request.POST["start_bid"],
            active_stat = True,
            creator=User.objects.get(username=request.user),
            created_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        listing.save()

        return HttpResponseRedirect(reverse("auctions:index"))

    return render(request, "auctions/create_list.html")

def view_list(request, title):    
    listing = Listing.objects.get(title=title)
    comments = listing.comments.all()

    return render(request, "auctions/view_list.html",{
        "view_list": listing,
        "watchlists": WatchList.objects.filter(watcher_name=request.user).values_list('listing__title', flat=True),
        "comments": comments
    })

def close_auc(request, title):
    listing = Listing.objects.get(title=title)

    listing.active_stat = False
    listing.bid_winner=str(Bid.objects.get(listing=title).bidder)

    listing.save()
    
    return HttpResponseRedirect(reverse("auctions:view_list",args=[title]), {
        "view_list": listing,
        "watchlists": WatchList.objects.filter(watcher_name=request.user).values_list('listing__title', flat=True),
        "comments": listing.comments.all()
    })

################################################################################################### 

def bid(request, title):
    if request.method == "POST":
        listing = Listing.objects.get(title=title)
        
        try:
            bid = Bid.objects.get(listing = listing.title)
            bid.bidder = User.objects.get(username=request.user)
            bid.value = int(request.POST["bid_value"])

        except:
            bid = Bid(
                listing = listing.title,
                bidder = User.objects.get(username=request.user),
                value = int(request.POST["bid_value"])
            )

        listing.bid_counter += 1
        listing.bid_value = int(request.POST["bid_value"])
        
        listing.save()
        bid.save()

    return HttpResponseRedirect(reverse("auctions:view_list",args=[title]), {
        "view_list": listing,
        "watchlists": WatchList.objects.filter(watcher_name=request.user).values_list('listing__title', flat=True),
        "comments": listing.comments.all()
    })

################################################################################################### 
def watchlist(request):
    watchlists = WatchList.objects.filter(watcher_name=request.user)

    return render(request, "auctions/watchlist.html",{
        "watchlists": watchlists,
    })

def mod_watchlist(request,title):
    listing = Listing.objects.get(title=title)
    
    try:
        watchlist = WatchList.objects.get(listing=listing)
        watchlist.delete()
    except:
        watchlist = WatchList(
            listing = listing,
            watcher_name = request.user
        )

        watchlist.save()

    return HttpResponseRedirect(reverse("auctions:view_list",args=[title]), {
        "view_list": listing,
        "watchlists": WatchList.objects.filter(watcher_name=request.user).values_list('listing__title', flat=True),
        "comments": listing.comments.all()
    })
      
################################################################################################### 

def comment(request, title):
    if request.method == "POST":
        comment = Comment(
            commentor_name = request.user,
            list_title = title,
            comment = request.POST["comment"],
            commented_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        comment.save()

        listing = Listing.objects.get(title=title)
        listing.comments.add(comment)

        return HttpResponseRedirect(reverse("auctions:view_list",args=[title]), {
            "view_list": listing,
            "watchlists": WatchList.objects.filter(watcher_name=request.user).values_list('listing__title', flat=True),
            "comments": listing.comments.all()
        })

################################################################################################### 

def category(request):
    category_list = []

    for listing in Listing.objects.all():
        category_list.append(str(listing.category))

    category_list=list(set(category_list))

    return render(request, "auctions/categories.html",{
        "categories": category_list
    })

def view_cat(request, category):
    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/cat_list.html", {
        "category": category,
        "listings": listings
    })
