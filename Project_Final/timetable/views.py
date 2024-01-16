from django.contrib.auth import authenticate, login, logout
from django.core.serializers import serialize
from django.contrib.auth.decorators import login_required  # Import the login_required decorator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q

from .models import User, Event, Holiday
from . import holidays as h
from datetime import datetime, timedelta
import json

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
    h.add_update_holidays()

    # filters for holidays where the start_date is less than or equal to the current time and the
    # end_date is greater than or equal to the current time, which effectively checks if the current
    # date falls within the range of the holiday
    current_datetime = timezone.localtime(timezone.now())
    current_weekday = current_datetime.weekday()

    start_of_week = current_datetime - timedelta(days=current_datetime.weekday())
    end_of_week = start_of_week + timedelta(days=6)

    holidays = Holiday.objects.filter(
        start_date__date__in=[current_datetime],
        end_date__date__in=[current_datetime]
    )

    print(current_datetime, current_weekday)
    print(start_of_week)
    print(end_of_week)

    events = Event.objects.filter(
        user=request.user,
        start_date__range=[start_of_week, end_of_week],
        end_date__range=[start_of_week, end_of_week]
    )

    # modified_events = {idx:[] for idx in range(7)}

    # for event in events:
    #     event_start_weekday = event.start_date.weekday()
    #     event_end_weekday = event.end_date.weekday()

    #     for day in range(event_start_weekday, event_end_weekday + 1):
    #         modified_events[day].append(serialize('json', [event]))

    return render(request, "timetable/mainTable.html", {
                        "holidays": holidays,
                        "modified_events_json": events,
                    }
                )

def newEvent(request):
    return render(request, "timetable/newEvent.html")

@login_required  # Add the login_required decorator to ensure the user is authenticated
def existEvent(request):

    upcoming_events, past_events = [], []

    for event in Event.objects.filter(user=request.user):

        # Make event.end_datetime timezone-aware
        end_date_aware = event.end_datetime if timezone.is_aware(event.end_datetime) else timezone.make_aware(event.end_datetime, timezone.get_current_timezone())

        if timezone.now() <= end_date_aware:
            upcoming_events.append({
                "name": event.name,
                "description": event.event_description,
                "start_date": event.start_datetime,
                "end_date": event.end_datetime
            })
        else:
            past_events.append({
                "name": event.name,
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
                name = request.POST["event_name"],
                event_description = request.POST["event_description"],
                start_datetime = datetime.strptime(f"{request.POST['start_date']} {request.POST['start_time']}", "%Y-%m-%d %H:%M"),
                start_date=datetime.strptime(request.POST['start_date'], "%Y-%m-%d").date(),
                start_time=datetime.strptime(request.POST['start_time'], "%H:%M").time(),
                end_datetime = datetime.strptime(f"{request.POST['end_date']} {request.POST['end_time']}", "%Y-%m-%d %H:%M"),
                end_date=datetime.strptime(request.POST['end_date'], "%Y-%m-%d").date(),
                end_time=datetime.strptime(request.POST['end_time'], "%H:%M").time(),
            )

            event.save()
        else:
            print("User is not authenticated")

    return HttpResponseRedirect(reverse("timetable:mainTable"))

def feed(request):
    events = Event.objects.all().order_by('created_datetime')

    return render(request, "timetable/feed.html", {
        "events": events
    })