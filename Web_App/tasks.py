from Web_App.models import Server
from celery import shared_task

@shared_task
def stop_expired_containers():
    servers = Server.objects.all()
    for server in servers:
        if server.is_expired():
            server.stop_expired()
