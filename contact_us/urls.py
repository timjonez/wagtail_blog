from django.urls import path
from django.contrib import admin
from . import views

app_name = 'contact_us'

urlpatterns = [
    path('contactform/', views.emailView, name='email'),
]
