# Generated by Django 3.1.3 on 2021-05-29 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bakpak_website', '0002_remove_coordinatesmapdb_url_coordinates'),
    ]

    operations = [
        migrations.AddField(
            model_name='coordinatesmapdb',
            name='url_coordinates',
            field=models.CharField(default='Null', max_length=500),
        ),
    ]
