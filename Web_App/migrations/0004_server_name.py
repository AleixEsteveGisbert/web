# Generated by Django 4.1 on 2023-04-22 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web_App', '0003_alter_game_created_at_alter_game_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='name',
            field=models.TextField(default='Server'),
        ),
    ]