import docker
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from docker.errors import DockerException


def game_images_path(filename):
    # file will be uploaded to MEDIA_ROOT/games/game_<filename>
    return 'games/game_{0}'.format(filename)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Game(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to=game_images_path, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Server(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.TextField(default="Server")
    password = models.TextField(null=True)
    docker_name = models.TextField(null=True)
    address = models.TextField(default="localhost", null=True)
    port = models.IntegerField(default=0, null=True)
    version = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    cores = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    ram = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    storage = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.TextField(null=True)
    expiration_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def is_expired(self):
        if self.expiration_date is None:
            return False
        current_time = timezone.now()
        return self.expiration_date < current_time

    def stop_expired(self):
        if self.is_expired():
            try:
                client = docker.from_env()
            except DockerException as e:
                print("[Error] stop_if_expired: " + e.__str__())
                raise Exception("Docker is not running")
            try:
                container = client.containers.get(str(self.id))
                container.stop()
                self.status = "Stopped"
                self.save()
            except DockerException as e:
                print("[Error] stop_if_expired: " + e.__str__())
                raise Exception("Docker is not running")

