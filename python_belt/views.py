# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
from django.db.models import Count

# helper function to get current user id
def current_user(request):
    return User.objects.get(id = request.session["user_id"])


def index(request):
    print "-= Reached / (index.html) =-"
    print request.session.items()
    return render(request, "python_belt/index.html")

def createUser(request):
    print "-= Reached /users/create (redirect to friends.html) =-"
    if request.method != "POST":
        return redirect("/")

    # validate user reg fields
    check = User.objects.validateUserReg(request.POST)
    if check["pass"] is False:
        for error in check["errors"]:
            messages.error(request, error)
        return redirect("/")

    # create user via create_user function
    user = User.objects.create_user(request.POST)
    print User.objects.all()
    # created user into db, add user id to session to log in
    request.session["user_id"] = user.id
    return redirect("/friends")


def loginUser(request):
    print "-= Reached /login (redirect to friends.html) =-"
    if request.method != "POST":
        return redirect("/")

    # validate login via validateUserLog from models.py
    check = User.objects.validateUserLog(request.POST)
    if check["pass"] is False:
        messages.error(request, check["errors"])
        return redirect("/")

    # valid email, password for login, store user id to session, go to friends.html
    request.session["user_id"] = check["user"].id
    return redirect("/friends")

def friends(request):
    print "-= Reached /friends (friends.html) =-"
    # verify user is registered or logged with session user_id to reach friends.html
    if "user_id" not in request.session:
        return redirect("/")
    this_user = current_user(request)
    user_friends = this_user.friends.all()
    num_friends = len(user_friends)
    user_friends_id_lst = user_friends.values_list('id', flat = True)
    other_users = User.objects.exclude(id = this_user.id).exclude(id__in = user_friends_id_lst)

    data = {
        "this_user": this_user,
        "user_friends": user_friends,
        "other_users": other_users,
        "num_friends": num_friends,
    }
    return render(request, "python_belt/friends.html", data)

def logoutUser(request):
    print "-= Reached /users/logout (redirect to /) =-"
    request.session.clear()
    return redirect("/")

def addFriend(request, user_id):
    print "-= Reached friends/add/<user_id> (redirect to /friends) =-"
    if request.method != "POST":
        return redirect("/")

    curr_user = current_user(request)
    this_user = User.objects.filter(id = user_id).first()
    curr_user.friends.add(this_user)

    return redirect("/friends")

def removeFriend(request, friend_id):
    print "-= Reached friends/remove/<friend_id> (redirect to /friends) =-"

    curr_user = current_user(request)
    this_friend = User.objects.filter(id = friend_id).first()
    curr_user.friends.remove(this_friend)

    return redirect("/friends")

def showUser(request, user_id):
    print "-= Reached /users/<user_id> (user.html) =-"
    this_user = User.objects.filter(id = user_id).first()
    data = {
        "user": this_user
    }

    return render(request, "python_belt/user.html", data)
