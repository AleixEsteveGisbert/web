import sys
from time import sleep

import websocket
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from docker.errors import DockerException
from docker.models.networks import Network

from Web_App.forms import LoginForm, RegisterForm, NewServerForm, MinecraftServerPropertiesForm
from Web_App.models import Game, Server
import docker

from django.http import HttpResponse
from web3 import Web3
from mcstatus import JavaServer

# https://www.geeksforgeeks.org/django-templates/

MCport = '25565'


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
            memory_limit = '1G'

            try:
                client = docker.from_env()
            except DockerException:
                print("Docker is not running")
                raise Exception("Docker is not running")

            server.save()
            try:
                container = client.containers.run(
                    'itzg/minecraft-server',
                    name=server.id,
                    ports={f'{MCport}/tcp': None, f'{MCport}/udp': None},
                    environment={
                        'EULA': 'TRUE',
                        'OVERRIDE_SERVER_PROPERTIES': 'false',
                        'VERSION': 'latest',
                        'MEMORY': memory_limit,
                        'SERVER_NAME': server.name,
                        'MOTD': "Welcome to server " + server.name,

                    },
                    detach=True,
                )
                # Configurem un sleep per a esperar fins que el contenidor estigui funcionant per a poder obtenir el port
                timeout = 120
                stop_time = 3
                elapsed_time = 0
                while container.status != 'running' and elapsed_time < timeout:
                    sleep(stop_time)
                    elapsed_time += stop_time
                    container.reload()
                    continue
                # Agafem tots els ports del contenidor
                ports = container.attrs['NetworkSettings']['Ports']
                # I ens quedem amb el port TCP
                server.port = ports[f'{MCport}/tcp'][0]['HostPort']
                server.status = "Running"
                server.save()
            except DockerException as e:
                server.delete()
                print("[Error] new_server: " + e.__str__())
                raise Exception("Error running server")
            return redirect('dashboard')
    else:
        form = NewServerForm()

    return render(request, 'controlPanel/server-new.html', {'form': form, 'games': games})


def getFile(path, container):
    command_read = f'cat {path}'
    result = container.exec_run(command_read)
    current_content = result.output.decode('utf-8')
    return current_content


def updateFile(data, path, container):
    command_write = f'echo "{data}" > {path}'
    result = container.exec_run(command_write, detach=False)  # TODO
    return result.exit_code


@login_required(login_url='login')
def details_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException:
            server.status = "Stopped"
            server.save()
            print("[Error] details_server: Docker is not running")
            raise Exception("Docker is not running")
        container = client.containers.get(str(server.id))

        if request.method == 'POST':
            form = MinecraftServerPropertiesForm(request.POST)
            if form.is_valid():
                server_properties = form.cleaned_data['server_properties']
                updateFile(server_properties, '/data/server.properties', container)
                return redirect('server-edit', server.id)
        else:
            form = MinecraftServerPropertiesForm()
            if container.status == "running":
                server.status = "Running"
                serverproperties = getFile('/data/server.properties', container)
                form = MinecraftServerPropertiesForm(initial={'server_properties': serverproperties})
            else:
                server.status = "Stopped"
            details = None

            try:
                details = JavaServer.lookup(server.address + ":" + str(server.port)).status()
            except Exception as e:
                print(f"[Error] details_server: {e} - ({server.name})")

            context = {
                'form': form,
                'server': server,
                'details': details,
                'container': container,
            }
    else:
        return HttpResponse(status=403)
    return render(request, 'controlPanel/server-details.html', context)


@login_required(login_url='login')
def stop_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException:
            print("[Error] stop_server: Docker is not running")
            raise Exception("Docker is not running")
        try:
            container = client.containers.get(str(server.id))
            container.stop()
            server.status = "Stopped"
            server.save()
        except DockerException:
            print("[Error] stop_server: Can't stop server")
            raise Exception("Docker is not running")
    else:
        return HttpResponse(status=403)
    return redirect('server-edit', server.id)


@login_required(login_url='login')
def update_servers(request):
    servers = request.user.server_set.all()
    for server in servers:
        try:
            client = docker.from_env()
            container = client.containers.get(str(server.id))
            if container.status == "running":
                server.status = "Running"
            else:
                server.status = "Stopped"
            server.save()

        except DockerException as e:
            print(f"[Error] update_servers: {e}")
            raise Exception(e)
    return redirect("/dashboard")


@login_required(login_url='login')
def start_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException as e:
            print("[Error] start_server: Docker is not running")
            raise Exception("Docker is not running")
        container = client.containers.get(str(server.id))
        try:
            container.start()
            # Configurem un sleep per a esperar fins que el contenidor estigui funcionant per a poder obtenir el port
            timeout = 120
            stop_time = 3
            elapsed_time = 0
            while container.status != 'running' and elapsed_time < timeout:
                sleep(stop_time)
                elapsed_time += stop_time
                container.reload()
                continue

            server.status = "Running"
            # Agafem tots els ports del contenidor
            ports = container.attrs['NetworkSettings']['Ports']
            # I ens quedem amb el port TCP
            server.port = ports[f'{MCport}/tcp'][0]['HostPort']
            server.save()
        except DockerException as e:
            print("[Error] start_server: " + e.__str__())
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=403)
    return redirect(f"/server/{server.id}/details")


@login_required(login_url='login')
def restart_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException as e:
            print("[Error] start_server: Docker is not running")
            raise Exception("Docker is not running")
        container = client.containers.get(str(server.id))
        try:
            container.restart()
            sleep(3)
            container.reload()
            # Configurem un sleep per a esperar fins que el contenidor estigui funcionant per a poder obtenir el port
            timeout = 120
            stop_time = 3
            elapsed_time = 0
            while elapsed_time < timeout and container.status != 'running':
                sleep(stop_time)
                elapsed_time += stop_time
                container.reload()
                continue

            server.status = "Running"
            # Agafem tots els ports del contenidor
            ports = container.attrs['NetworkSettings']['Ports']
            # I ens quedem amb el port TCP
            server.port = ports[f'{MCport}/tcp'][0]['HostPort']
            server.save()
        except DockerException as e:
            print("[Error] restart_server: " + e.__str__())
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=403)
    return redirect('server-edit', server.id)


@login_required(login_url='login')
def delete_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException:
            print("[Error] start_server: Docker is not running")
            raise Exception("Docker is not running")
        container = client.containers.get(str(server.id))
        try:
            container.stop()
            container.remove(True)
        except DockerException as e:
            print("[Error] delete_server: " + e.__str__())
            return HttpResponse(status=500)
        server.delete()
    else:
        return HttpResponse(status=403)
    return redirect('dashboard')


@login_required(login_url='login')
def wallet(request):
    sepolia = 'https://eth-sepolia.g.alchemy.com/v2/5APA3WpSw2ESkV84Qlcy-4ZgFQW9I9_M'
    web3 = Web3(Web3.HTTPProvider(sepolia))

    wa = '0xF24F56a34D16B7a1FB2F6f9dbb160911565873f2'
    balance = web3.from_wei(web3.eth.get_balance(wa), 'ether')
    context = {
        'balance': balance,
    }
    return render(request, 'controlPanel/wallet.html', context)
