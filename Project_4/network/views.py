from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import User, Post

import json

def index(request):
    paginator = Paginator(Post.objects.all().order_by("-created_datetime"), 10)
    page = request.GET.get("page")

    return render(request, "network/index.html", {
        "active_posts": Post.objects.all().order_by("-created_datetime"),
        "posts": paginator.get_page(page)
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

    paginator = Paginator(Post.objects.filter(creator=user).order_by("-created_datetime"), 10)
    page = request.GET.get("page")
    
    return render(request, "network/profile.html", {
        "user": user,
        "posts": paginator.get_page(page),
    })

def follow_user(request, name):
    follower = get_object_or_404(User, username=request.user)
    following = get_object_or_404(User, username=name)
    
    if not follower.following.filter(pk=following.pk).exists():
        follower.following.add(following)
        following.followers.add(follower)    
    else:
        follower.following.remove(following)
        following.followers.remove(follower)

    follower.save()
    follower.save()

    return HttpResponseRedirect(reverse("network:user_profile", args=[name]))

#################################################################################################

def following(request):
    user = get_object_or_404(User, username=request.user)

    #"following_users" is a queryset of user objects and cannot be directly used as a value in the creator field filter.
    following_users = user.following.all()
    # "__in" lookup is used to filter posts whose creator is one of the users in the "following_users" queryset
    paginator = Paginator(Post.objects.filter(creator__in=following_users).order_by('created_datetime'), 10)
    page = request.GET.get("page")

    return render(request, "network/following.html", {
        "posts": paginator.get_page(page),
    })

#################################################################################################

@csrf_exempt 
def update_postcontent(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)  
            
            post = Post.objects.get(pk = int(data["id"]))
            post.content = data["data"]

            post.save()
            
            # Process the data 
            response_data = {"message": "Database updated successfully", "data":{
                'id': post.id,
                'creator': post.creator.username,
                'content': post.content,
                'created_datetime': post.created_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'likes': post.likes,
            }}
            return JsonResponse(response_data)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

#################################################################################################

@csrf_exempt 
def update_likes(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)  

            post = Post.objects.get(pk = int(data["id"]))
            
            if data["like_post"]:
                post.likes += 1
            else:
                post.likes -= 1

            post.save()
            
            # Process the data 
            response_data = {"message": "Database updated successfully", "data":{
                'id': post.id,
                'creator': post.creator.username,
                'content': post.content,
                'created_datetime': post.created_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'likes': post.likes,
            }}
            return JsonResponse(response_data)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)