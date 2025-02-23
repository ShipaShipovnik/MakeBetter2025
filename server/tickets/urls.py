from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-ticket/', views.create_ticket, name='create-ticket'),
    # для формы
    path('create-category/', views.create_category, name='create-catg'),
    path('delete-catg/', views.delete_category, name='delete-catg'),
    #
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
]
