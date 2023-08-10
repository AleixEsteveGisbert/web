from background_task import background

from Web_App.models import Server


@background(schedule=60)
def stop_expired_containers():
    servers = Server.objects.all()
    for server in servers:
        if server.is_expired():
            server.stop_expired()
