from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r"^$", views.index),
    url(r"^users/create$", views.createUser),
    url(r"^home$", views.home),
    url(r"^users/login$", views.loginUser),
    url(r"^users/logout$", views.logout),

]
