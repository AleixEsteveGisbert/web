# Generated by Django 4.2 on 2023-08-03 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Web_App', '0013_alter_server_cores'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='cores',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]