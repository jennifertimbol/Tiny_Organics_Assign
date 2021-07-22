from django.urls import path
from . import views

urlpatterns = [
path('', views.index),
path('register', views.register),
path('login', views.login),
path('fetch_allergens', views.fetch_allergens),
path('homepage', views.homepage),
path('fetchrecipes', views.fetchrecipes),
path('results/<int:child_id>', views.results),
path('generaterecipes', views.generate_recipes),
path('logout', views.logout)
]