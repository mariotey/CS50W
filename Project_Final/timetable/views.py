from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import AnonymousUser
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from.models import User
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, "timetable/login.html")

#################################################################################################

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            print("Login successful")

            ## Add in logic to populate mainTable with specific user data
            
            return render(request, "timetable/mainTable.html")
        else:
            print("Login unsuccessful")
            return render(request, "timetable/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "timetable/login.html")

def logout_view(request):
    logout(request)

    if isinstance(request.user, AnonymousUser):
       print("Logout was successful")
       logger.info(f"User {request.user} has been logged out.")
    else:
        print("Logout was unsuccessful")
        logger.error("Logout failed. User is still authenticated.")

    return HttpResponseRedirect(reverse("timetable:login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "timetable/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "timetable/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("timetable:index"))
    else:
        return render(request, "timetable/register.html")

#################################################################################################

def mainTable(request):
    return render(request, "timetable/mainTable.html")

def createEvent(request):
    return render(request, "timetable/event.html")