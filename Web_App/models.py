from django.db import models


# Create your models here.
class Wallet(models.Model):
    balance = models.DecimalField(decimal_places=8, max_digits=12)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Foreign key
    #idUser = models.ForeignKey(User, on_delete=models.CASCADE)


class User(models.Model):
    name = models.TextField(null=True)
    surname = models.TextField(null=True)
    email = models.TextField()
    username = models.TextField(null=True)
    password = models.TextField()
    avatar = models.TextField(null=True)
    enabled = models.BooleanField(default=True)
    id_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Server(models.Model):
    game = models.TextField()
    version = models.DecimalField(decimal_places=2, max_digits=8)
    cores = models.DecimalField(decimal_places=2, max_digits=8)
    ram = models.DecimalField(decimal_places=2, max_digits=8)
    storage = models.DecimalField(decimal_places=2, max_digits=8)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
