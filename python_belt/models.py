# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import re, bcrypt
from datetime import datetime

def validateDate(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class UserManager(models.Manager):
    def validateUserReg(self, post_data):
        valid = True
        error_msgs = []

        if len(post_data["name"]) < 2 or not post_data["name"].isalpha():
            valid = False
            error_msgs.append("Name must be at least 2 characters and only letters.")
        if len(post_data["alias"]) < 2:
            valid = False
            error_msgs.append("Alias must be at least 2 characters.")
        if not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", post_data["email"]):
            valid = False
            error_msgs.append("Invalid e-mail.")
        if User.objects.filter(email = post_data["email"]).first():
            valid = False
            error_msgs.append("E-mail already in use.")
        if len(post_data["password"]) < 8:
            valid = False
            error_msgs.append("Passwords must be at least 8 characters long.")
        if post_data["password"] != post_data["confirm_pwd"]:
            valid = False
            error_msgs.append("Passwords don't match.")
        if len(post_data["birthdate"]) < 1:
            valid = False
            error_msgs.append("Birthdate can't be blank.")

        # validate birthdate
        birthdate = str(post_data["birthdate"])
        if validateDate(birthdate):
            # convert user form date to datetime object for calculating time delta
            birthdate_date_obj = datetime.strptime(birthdate, "%Y-%m-%d")
            age_days = (datetime.now() - birthdate_date_obj).days
            if age_days < 0:
                error_msgs.append("Invalid birthdate.")
            age_yrs = age_days/365
            if age_yrs < 13:
                error_msgs.append("You must be at least 13 years old to register an account.")
        # fails validateDate with improper date format
        else:
            error_msgs.append("Invalid birthdate.")

        return {"pass": valid, "errors": error_msgs}


    def create_user(self, post_data):
        hashed_pwd = bcrypt.hashpw(post_data["password"].encode(), bcrypt.gensalt())
        return User.objects.create(
            name = post_data["name"],
            alias = post_data["alias"],
            email = post_data["email"],
            password = hashed_pwd,
            birthdate = post_data["birthdate"],
        )


    def validateUserLog(self, post_data):
        # verify if email, password is blank
        if len(post_data["email"]) < 1 or len(post_data["password"]) < 1:
            return {"pass": False, "errors": "Login credentials can't be blank."}

        # verify email, password against db for valid user
        user = User.objects.filter(email = post_data["email"]).first()
        if user and bcrypt.checkpw(post_data["password"].encode(), user.password.encode()):
            return {"pass": True, "user": user}

        return {"pass": False, "errors": "Invalid login credentials."}

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    birthdate = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

    def __str__(self):
        return "Name: {}, Alias: {}, e-mail: {}, Password: {}, Birthdate: {}".format(self.name, self.alias, self.email, self.password, self.birthdate)
