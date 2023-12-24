from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import User, Event, Holiday
from . import holidays
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

            return redirect(reverse("timetable:mainTable"))
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
    print(request)

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        print(username)

        if password != confirmation:
            return render(request, "timetable/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)

            login(request, user)

            return HttpResponseRedirect(reverse("timetable:mainTable"))

        except IntegrityError:
            return render(request, "timetable/register.html", {
                "message": "Username or email already taken."
            })

        except Exception as error:
            print(error)

    else:
        return render(request, "timetable/register.html")

#################################################################################################

def mainTable(request):
    # Update Holiday in database
    holidays.add_update_holidays()

    # filters for holidays where the start_date is less than or equal to the current time and the
    # end_date is greater than or equal to the current time, which effectively checks if the current
    # date falls within the range of the holiday
    holiday =  Holiday.objects.filter(start_date__lte=timezone.now(), end_date__gte=timezone.now())

    print(holiday)

    return render(request, "timetable/mainTable.html", {"holiday": holiday})

def newEvent(request):
    return render(request, "timetable/newEvent.html")

@login_required  # Add the login_required decorator to ensure the user is authenticated
def existEvent(request):

    upcoming_events, past_events = [], []

    for event in Event.objects.filter(user=request.user):
        # Make event.end_datetime timezone-aware
        end_datetime_aware = event.end_datetime if timezone.is_aware(event.end_datetime) else timezone.make_aware(event.end_datetime, timezone.get_current_timezone())

        if timezone.now() <= end_datetime_aware:
            upcoming_events.append({
                "name": event.event_name,
                "description": event.event_description,
                "start_date": event.start_datetime,
                "end_date": event.end_datetime
            })
        else:
            past_events.append({
                "name": event.event_name,
                "description": event.event_description,
                "start_date": event.start_datetime,
                "end_date": event.end_datetime
            })

    print(upcoming_events,"\n")
    print(past_events, "\n")

    return render(request, "timetable/events.html", {
        "upcoming": upcoming_events,
        "past": past_events
    })

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