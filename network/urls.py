
from django.urls import path
from django.urls.conf import re_path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    re_path(r'^profile/(?P<user_slug>[\w-]+)$', views.profile, name="profile"),
    re_path(r'^following/(?P<user_slug>[\w-]+)$', views.following, name="following"),
    re_path(r'^like[/]?(?P<pk>[\d]+)?$', views.like, name="like"),
    re_path(r'^follow[/]?(?P<pk>[\d]+)?$', views.follow, name="follow"),
    re_path(r'^lastlikes$', views.last_likes, name="last-likes"),
    re_path(r'^post', views.post, name="post"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
