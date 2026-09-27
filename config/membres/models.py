from django.db import models

# Create your models here.
class Emprunteur(models.Model):
    nom = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nom} ({self.email})"
