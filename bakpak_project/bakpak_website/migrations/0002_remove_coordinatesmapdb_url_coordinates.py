# Generated by Django 3.1.3 on 2021-05-29 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bakpak_website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coordinatesmapdb',
            name='url_coordinates',
        ),
    ]
