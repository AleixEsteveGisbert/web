# Generated by Django 4.2 on 2023-08-07 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web_App', '0014_alter_server_cores'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='expiration_date',
            field=models.DateTimeField(null=True),
        ),
    ]