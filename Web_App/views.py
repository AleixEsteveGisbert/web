import sys

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from docker.errors import DockerException

from Web_App.forms import LoginForm, RegisterForm, NewServerForm
from Web_App.models import Game, Server
import docker

from mcstatus import JavaServer


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
            server.user = request.user
            server.game_id = request.POST.get('game')

            port = '25565'
            memory_limit = '1G'

            try:
                client = docker.from_env()
            except DockerException:
                print("Docker is not running")
                raise Http404("Docker is not running")

            server.save()
            try:
                container = client.containers.run(
                    'itzg/minecraft-server',
                    name=server.id,
                    ports={f'{port}/tcp': None, f'{port}/udp': None},
                    environment={
                        'EULA': 'TRUE',
                        'VERSION': 'latest',
                        'MEMORY': memory_limit,
                    },
                    detach=True,
                )
            except DockerException as e:
                print("[Error] new_server: " + e.__str__())
                raise Http404("Error running server")
            return redirect('dashboard')
    else:
        form = NewServerForm()

    return render(request, 'controlPanel/server-new.html', {'form': form, 'games': games})


@login_required(login_url='login')
def show_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)

    try:
        client = docker.from_env()
    except DockerException:
        print("Docker is not running")
        raise Http404("Docker is not running")

    container = client.containers.get(server.id)
    container_ip = container.attrs['NetworkSettings']['IPAddress']
    context = {
        'server': server,
        'container_ip': container_ip

    }
    return render(request, 'controlPanel/server-show.html', context)


@login_required(login_url='login')
def details_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    try:
        client = docker.from_env()
    except DockerException:
        print("Docker is not running")
        raise Http404("Docker is not running")

    container = client.containers.get(str(server.id))
    container_ip = container.attrs['NetworkSettings']['IPAddress']
    running = True
    details = None
    try:
        details = JavaServer.lookup(server.address).status()
    except Exception as e:
        running = False
        print(f"Error: {e} - Can't connect to Minecraft Server ({server.name})")

    context = {
        'server': server,
        'details': details,
        'running': running,
        'container': container,
        'container_ip': container_ip,
    }

    return render(request, 'controlPanel/server-details.html', context)


@login_required(login_url='login')
def stop_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException:
            print("Docker is not running")
            raise Http404("Docker is not running")
        container = client.containers.get(str(server.id))
        container.stop()
    return HttpResponseRedirect(f"/server/{server.id}/details")


@login_required(login_url='login')
def start_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException:
            print("Docker is not running")
            raise Http404("Docker is not running")
        container = client.containers.get(str(server.id))
        try:
            container.start()
        except DockerException as e:
            print("[Error] start_server: " + e.__str__())
            return HttpResponse(status=500)
    return HttpResponseRedirect(f"/server/{server.id}/details")
