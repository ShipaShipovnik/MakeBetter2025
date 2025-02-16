from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
]
