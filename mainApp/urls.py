from django.urls import path
from . import views

urlpatterns = [
path('', views.index),
path('register', views.register),
path('login', views.login),
path('homepage', views.homepage),
path('fetchrecipes', views.fetch_recipes),
path('results/<int:child_id>', views.results),
path('logout', views.logout)
]