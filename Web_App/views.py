from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from Web_App.forms import LoginForm, RegisterForm


# Create your views here.
# https://www.geeksforgeeks.org/django-templates/
def main_page(request):
    context = {

    }
    return render(request, 'mainPage/mainPage.html', context)

def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'mainPage/register.html', {'form': form})

def login_form(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'mainPage/login.html', {'form': form})

