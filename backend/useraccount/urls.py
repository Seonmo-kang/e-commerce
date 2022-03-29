from unicodedata import name
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.test, name="index"),
    path('login/', views.loginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name= "register"),
    path('homepage/',views.homepage, name='homepage')
]