from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class NewsletterDB(models.Model):
    email = models.EmailField(default="test@gmail.com")


class CoordinatesMapDB(models.Model):
    CHOICES = (
        ('Brasserie', 'Brasserie Bakpaker'),
        ('Restaurant', 'Restaurant'),
        ('Bar', 'Bar'),
        ('Marche', 'Marché')
    )
    url_coordinates = models.CharField(max_length=500, default="N/A")
    name_of_locations = models.CharField(max_length=300)
    adresse = models.CharField(max_length=300)
    code_postal = models.CharField(max_length=300)
    localite = models.CharField(max_length=300)
    categories = models.CharField(max_length=300, choices=CHOICES, default="Brasserie")
    informations_supplementaires = HTMLField()

