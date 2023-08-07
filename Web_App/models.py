from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def game_images_path(filename):
    # file will be uploaded to MEDIA_ROOT/games/game_<filename>
    return 'games/game_{0}'.format(filename)


# Create your models here.
class Wallet(models.Model):
    balance = models.DecimalField(decimal_places=8, max_digits=12, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField(null=True)
    wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Game(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to=game_images_path, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class Server(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.TextField(default="Server")
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


class ConsoleMessage(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
