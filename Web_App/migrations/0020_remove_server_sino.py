# Generated by Django 4.2 on 2023-08-28 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Web_App', '0019_server_sino'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='sino',
        ),
    ]