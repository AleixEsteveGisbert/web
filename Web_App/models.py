from django.contrib.auth.models import User
from django.db import models


def game_images_path(filename):
    # file will be uploaded to MEDIA_ROOT/games/game_<filename>
    return 'games/game_{0}'.format(filename)
# Create your models here.
class Wallet(models.Model):
    balance = models.DecimalField(decimal_places=8, max_digits=12, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.TextField(null=True)
    id_wallet = models.OneToOneField(Wallet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Game(models.Model):
    name = models.TextField()
    image = models.ImageField(upload_to=game_images_path, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Server(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    version = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    cores = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    ram = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    storage = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

