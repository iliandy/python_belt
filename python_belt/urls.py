from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r"^$", views.index),
    url(r"^users/create$", views.createUser),
    url(r"^friends$", views.friends),
    url(r"^users/login$", views.loginUser),
    url(r"^users/logout$", views.logoutUser),
    url(r"^friends/add/(?P<user_id>\d+)$", views.addFriend),
    url(r"^friends/remove/(?P<friend_id>\d+)$", views.removeFriend),
    url(r"^users/(?P<user_id>\d+)$", views.showUser),

]
