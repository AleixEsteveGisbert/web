import datetime
import json
import random
import string
from time import sleep

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from docker.errors import DockerException
from django.http import JsonResponse

from Web_App.forms import LoginForm, RegisterForm, NewServerForm, MinecraftServerPropertiesForm, addDaysForm
from Web_App.models import Game, Server
import docker

from django.http import HttpResponse, HttpRequest
from web3 import Web3
from mcstatus import JavaServer

MCport = '25565'
ValheimPort = ['2456', '2457']


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
            try:
                client = docker.from_env()
            except DockerException as e:
                print("Docker is not running")
                raise Exception(f"[Error] new_server: {e.__str__()}")
            server.save()
            if server.id < 10:
                server.delete()
                server.id = 10
            if server.game.name == "Minecraft":
                try:
                    memory_limit = '1G'
                    container = client.containers.run(
                        'itzg/minecraft-server',
                        name=server.id,
                        mem_limit=f"{server.ram}g",
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
                    server.expiration_date = timezone.now() + datetime.timedelta(days=1)
                    server.save()
                except DockerException as e:
                    server.delete()
                    print("[Error] new_server: " + e.__str__())
                    raise Exception("[Error] new_server: " + e.__str__())
                server.save()
            elif server.game.name == "Valheim":
                try:
                    password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                    server.password = password
                    container = client.containers.run(
                        "ghcr.io/lloesche/valheim-server",
                        name=server.id,
                        mem_limit=f"{server.ram}g",
                        ports={f'{ValheimPort[0]}/udp': None, f'{ValheimPort[1]}/udp': None},
                        cap_add="sys_nice",
                        volumes={
                            "/home/valheim-server/config": {'bind': '/config', 'mode': 'rw'},
                            "/home/valheim-server/data": {'bind': '/opt/valheim', 'mode': 'rw'}
                        },
                        environment={
                            "SERVER_NAME": server.name,
                            "WORLD_NAME": server.name,
                            "SERVER_PUBLIC": "true",
                            "SERVER_PASS": password,
                            "STATUS_HTTP": "true",
                            "SYSLOG_REMOTE_AND_LOCAL": "true"
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
                    server.port = ports[f'{ValheimPort[0]}/udp'][0]['HostPort']
                    server.status = "Running"
                    server.expiration_date = timezone.now() + datetime.timedelta(days=1)
                    server.save()
                except DockerException as e:
                    server.delete()
                    print("[Error] new_server: " + e.__str__())
                    raise Exception("[Error] new_server: " + e.__str__())
            elif server.game.name == "Terraria":
                pass

            return redirect('dashboard')
    else:
        form = NewServerForm()
        # contract.spend_host_coins(request, 1)
    return render(request, 'controlPanel/server-new.html', {'form': form, 'games': games})


# Function to read file content from a container

def getFile(path, container):
    try:
        command_read = f'cat {path}'
        result = container.exec_run(command_read)
        current_content = result.output.decode('utf-8')
    except Exception as e:
        current_content = None
        print(f"[Error] getFile: {e}")
    return current_content


# Function to update a content of a file in a container
def updateFile(data, path, container):
    try:
        command_write = f'bash -c "echo {data} > {path}"'
        result = container.exec_run(command_write, detach=False)
    except Exception as e:
        result = None
        print(f"[Error] updateFile: {e}")
    return result


def executeCommand(command, container):
    try:
        command_write = command
        result = container.exec_run(command_write, detach=False)
    except Exception as e:
        result = None
        print(f"[Error] executeCommand: {e}")
    return result

@login_required(login_url='login')
def executeCommandMinecraft(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
            container = client.containers.get(str(server.id))
        except DockerException as e:
            server.status = "Stopped"
            server.save()
            print(f"[Error] executeCommandMinecraft: {e.__str__()}")
            raise Exception(f"[Error] executeCommandMinecraft: {e.__str__()}")
        if request.method == 'POST':
            command = request.POST.get('command')
            command = f"mc-send-to-console {command}"
            executeCommand(command, container)
        return HttpResponse(status=200)
    return HttpResponse(status=500)

@login_required(login_url='login')
def details_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    console = ''
    context = ''
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException:
            server.status = "Stopped"
            server.save()
            print("[Error] details_server: Docker is not running")
            raise Exception("Docker is not running")
        container = client.containers.get(str(server.id))
        if server.game.name == "Minecraft":
            if request.method == 'POST':
                form = MinecraftServerPropertiesForm(request.POST)
                if form.is_valid():
                    server_properties = form.cleaned_data['server_properties']
                    res = updateFile(server_properties, '/data/server.properties', container)
                    print(res)
                    return redirect('server-edit', server.id)
            else:
                form = MinecraftServerPropertiesForm()
                if container.status == "running":
                    server.status = "Running"
                    serverproperties = getFile('/data/server.properties', container)
                    form = MinecraftServerPropertiesForm(initial={'server_properties': serverproperties})
                    console = getFile('/data/logs/latest.log', container)
                else:
                    server.status = "Stopped"
                details = None
                server.save()
                try:
                    details = JavaServer.lookup(server.address + ":" + str(server.port)).status()
                except Exception as e:
                    print(f"[Error] details_server: {e} - ({server.name})")
                context = {
                    'form': form,
                    'server': server,
                    'details': details,
                    'container': container,
                    'console': console,
                }
                if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
                    return JsonResponse({'content': console})

                return render(request, 'controlPanel/server-details-mc.html', context)

        elif server.game.name == "Valheim":
            serverInfo = None
            console = ""
            if container.status == "running":
                command = "bash -c 'ls /var/log/supervisor/valheim-server-stdout---supervisor-*.log'"
                res = executeCommand(command, container)
                res1 = res.output.decode("utf-8")
                console = getFile(res1, container)
                server.status = "Running"
                try:
                    serverInfo = getFile('/opt/valheim/htdocs/status.json', container)
                    serverInfo = json.loads(serverInfo)
                except Exception as e:
                    print(f"[Error] details_server:{e}")
            else:
                server.status = "Stopped"
            server.save()

            context = {
                'server': server,
                'container': container,
                'serverInfo': serverInfo,
                'console': console
            }
            return render(request, 'controlPanel/server-details-valheim.html', context)
    else:
        return HttpResponse(status=403)


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
        except DockerException as e:
            print(f"[Error] stop_server: {e}")
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
    return redirect('dashboard')


@login_required(login_url='login')
def start_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        if not server.is_expired():
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
                if server.game == "Minecraft":
                    server.port = ports[f'{MCport}/tcp'][0]['HostPort']
                elif server.game.name == "Valheim":
                    server.port = ports[f'{ValheimPort[0]}/udp'][0]['HostPort']
                server.save()
            except DockerException as e:
                print("[Error] start_server: " + e.__str__())
                return HttpResponse(status=500)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=403)
    return redirect('server-edit', server.id)


@login_required(login_url='login')
def restart_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        if not server.is_expired():
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
                if server.game == "Minecraft":
                    server.port = ports[f'{MCport}/tcp'][0]['HostPort']
                elif server.game.name == "Valheim":
                    server.port = ports[f'{ValheimPort[0]}/udp'][0]['HostPort']
                server.save()
            except DockerException as e:
                print("[Error] restart_server: " + e.__str__())
                return HttpResponse(status=500)
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=403)
    return redirect('server-edit', server.id)


@login_required(login_url='login')
def delete_server(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if server.user == request.user:
        try:
            client = docker.from_env()
        except DockerException as e:
            print(f"[Error] start_server: {e}")
            raise Exception(f"[Error] start_server: {e}")
        container = client.containers.get(str(server.id))
        try:
            container.stop()
            container.remove(v=True, force=True)
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


@login_required(login_url='login')
def adddays(request, server_id):
    server = get_object_or_404(Server, id=server_id)
    if request.method == 'POST':
        form = addDaysForm(request.POST)
        if form.is_valid():
            days = int(form.cleaned_data['days'])
            if server.expiration_date < timezone.now():
                server.expiration_date = datetime.datetime.now() + datetime.timedelta(days=days)
            else:
                server.expiration_date = server.expiration_date + datetime.timedelta(days=days)
            server.save()
            return redirect('server-edit', server.id)
    else:
        form = addDaysForm()

    context = {
        'server': server,
        'form': form,
    }
    return render(request, 'controlPanel/server-add-days.html', context)


@login_required(login_url='login')
@csrf_exempt
def set_expiration_date(request, server_id):
    if request.method == 'POST':
        server = get_object_or_404(Server, id=server_id)
        if request.user.id is server.user.id:
            print('1')
            if not server.expiration_date:
                print('2')
                server.expiration_date = datetime.datetime.now() + datetime.timedelta(days=1)
            else:
                server.expiration_date = server.expiration_date + datetime.timedelta(days=1)
            server.save()
        else:
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=400)
    return HttpResponse(status=200)
