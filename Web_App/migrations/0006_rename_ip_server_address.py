# Generated by Django 4.2 on 2023-04-27 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web_App', '0005_server_docker_name_server_ip_server_port'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='ip',
            new_name='address',
        ),
    ]
