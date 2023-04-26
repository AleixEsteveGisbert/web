import sys

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from Web_App.forms import LoginForm, RegisterForm, NewServerForm
from Web_App.models import Game, Server
import docker

client = docker.from_env()


# Create your views here.
# https://www.geeksforgeeks.org/django-templates/
def main_page(request):
    games = Game.objects.all()
    context = {
        'games': games
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


@login_required(login_url='login')
def dashboard(request):
    servers = request.user.server_set.all()
    context = {
        'servers': servers
    }
    return render(request, 'controlPanel/dashboard.html', context)


@login_required(login_url='login')
def new_server(request):
    games = Game.objects.all()
    if request.method == 'POST':
        form = NewServerForm(request.POST, request.FILES)
        if form.is_valid():
            server = form.save(commit=False)
            server.id_user = request.user
            server.game_id = request.POST.get('game')
            server.save()

            port = '25565'
            memory_limit = '1G'

            container = client.containers.run(
                'itzg/minecraft-server',
                name=server.id,
                ports={f'{port}/tcp': port, f'{port}/udp': port},
                environment={
                    'EULA': 'TRUE',
                    'VERSION': 'latest',
                    'MEMORY': memory_limit,
                },
                detach=True,
            )

            return redirect('dashboard')
    else:
        form = NewServerForm()

    return render(request, 'controlPanel/new-server.html', {'form': form, 'games': games})


def show_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    container = client.containers.get(str(server.id)+"_"+server.name)
    container_ip = container.attrs['NetworkSettings']['IPAddress']
    context = {
        'server': server,
        'container_ip': container_ip

    }
    return render(request, 'controlPanel/show-server.html', context)
