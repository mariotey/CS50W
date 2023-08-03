from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from datetime import datetime

from .models import User, Post

def index(request):
    return render(request, "network/index.html", {
        "active_posts": Post.objects.all().order_by("-created_datetime"),
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")

#################################################################################################

def submitpost(request):
    if request.method == "POST":
        post = Post(
            creator = request.user,
            content = request.POST["post_input"],
            created_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        post.save()

    return HttpResponseRedirect(reverse("network:index"))

def user_profile(request, name):
    user = get_object_or_404(User, username=name)
    
    return render(request, "network/profile.html", {
        "user": user,
        "posts": Post.objects.filter(creator=user).order_by("-created_datetime"),
    })