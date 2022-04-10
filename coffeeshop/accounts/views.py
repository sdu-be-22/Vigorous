from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from accounts.forms import CustomUserCreationForm
from shop.views import *

def indexView(request):
    return render(request, 'accounts/index.html')


@login_required()
def dashboardView(request):
    return render(request, 'accounts/dashboard.html')


from django.urls import reverse


def registerView(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Successfully Register')
            return redirect(reverse('register'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def loginView(request):
    return render(request, 'accounts/login.html')


def mainView(request):
    return render(request, 'accounts/main.html')
