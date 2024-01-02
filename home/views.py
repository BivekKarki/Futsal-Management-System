from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect


# Create your views here.
def homeview(request):
    return render(request, 'index.html')

@login_required
def welcomeview(request):
    context = {
        'welcome_message': 'hello'
    }
    return render(request, 'userDashboard.html',context)



