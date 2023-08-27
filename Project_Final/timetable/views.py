from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Event
from datetime import datetime

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

            return mainTable(request)
        else:
            print("Login unsuccessful")
            return render(request, "timetable/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "timetable/login.html")

def logout_view(request):
    logout(request)
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
    ## Add in logic to populate mainTable with specific user data

    return render(request, "timetable/mainTable.html")

def newEvent(request):
    return render(request, "timetable/newEvent.html")

@login_required  # Add the login_required decorator to ensure the user is authenticated
def createEvent(request):
    if request.method == "POST":
        
        if request.user.is_authenticated:
            
            event = Event(
                user = request.user,
                event_name = request.POST["event_name"],
                event_description = request.POST["event_description"],
                start_datetime = datetime.strptime(f"{request.POST['start_date']} {request.POST['start_time']}", "%Y-%m-%d %H:%M"),
                end_datetime = datetime.strptime(f"{request.POST['end_date']} {request.POST['end_time']}", "%Y-%m-%d %H:%M")
            )

            event.save()
        else:
            print("User is not authenticated")
    
    return HttpResponseRedirect(reverse("timetable:mainTable"))