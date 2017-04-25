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
    print "-= Reached /users/create (redirect to home.html) =-"
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
    return redirect("/home")


def loginUser(request):
    print "-= Reached /login (redirect to home.html) =-"
    if request.method != "POST":
        return redirect("/")

    # validate login via validateUserLog from models.py
    check = User.objects.validateUserLog(request.POST)
    if check["pass"] is False:
        messages.error(request, check["errors"])
        return redirect("/")

    # valid email, password for login, store user id to session, go to home.html
    request.session["user_id"] = check["user"].id
    return redirect("/home")

def home(request):
    print "-= Reached /home (home.html) =-"
    # verify user is registered or logged with session user_id to reach home.html
    if "user_id" not in request.session:
        return redirect("/")

    data = {
        "current_user": current_user(request),
    }
    return render(request, "python_belt/home.html", data)

def logout(request):
    print "-= Reached /users/logout (redirect to /) =-"
    request.session.clear()
    return redirect("/")
