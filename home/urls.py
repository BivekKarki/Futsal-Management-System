from django.contrib import admin
from django.urls import path, include

from home.views import homeview

app_name = "home"

urlpatterns = [
    path('', homeview, name='homepage'),


]
