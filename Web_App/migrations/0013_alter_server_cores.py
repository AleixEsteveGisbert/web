# Generated by Django 4.2 on 2023-08-03 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web_App', '0012_alter_server_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='cores',
            field=models.IntegerField(choices=[('1', '1'), ('2', '2'), ('4', '4')], null=True),
        ),
    ]
