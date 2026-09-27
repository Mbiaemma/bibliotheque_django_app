from django.db import models
from django.db.models import Model
from django.utils import timezone


# Create your models here.
class Auteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Genre(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "genres"

    def __str__(self):
        return self.nom

class Livre(models.Model):
    LANGUES = {
        "fr": "Français",
        "en": "Anglais",
        "it": "Italien",
    }

    titre = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, primary_key=True)
    nombre_pages = models.IntegerField()
    #blank=True parce que le champ est facultatif et null peut rester à false
    #parce que null=True n'est généralement utilise que pour les champs non texte
    resume = models.TextField(blank=True)
    #Ici pas besoin de définir blank et null car le champ a une valeur par défaut
    langue = models.CharField(max_length=2, choices=LANGUES, default="fr")
    #null=True et blank=True car le champ peut rester inconnu et est non textuel
    date_publication = models.DateField(blank=True, null=True)
    auteur = models.ForeignKey(Auteur, on_delete=models.CASCADE)
    genres = models.ManyToManyField(Genre, blank=True)
    emprunteurs = models.ManyToManyField("membres.Emprunteur",
                                         through="Emprunt",
                                         blank=True)

    class Meta:
        ordering = ['titre']

    def __str__(self):
        return self.titre

    @property
    def est_disponible(self):
        if self.emprunt_set.filter(date_retour_effective__isnull=True).exists():
            return False
        return True

    def save(self, **kwargs):
        self.titre = self.titre.title()
        super().save(**kwargs)


class Emprunt(models.Model):
    livre = models.ForeignKey(Livre, on_delete=models.CASCADE)
    emprunteur = models.ForeignKey("membres.Emprunteur", on_delete=models.CASCADE)
    date_emprunt = models.DateField(default=timezone.localdate)
    date_retour_prevue = models.DateField()
    date_retour_effective = models.DateField(blank=True, null=True)

    def __str__(self):
        etat = "rendu" if self.date_retour_effective else "en cours"
        return f"{self.livre} → {self.emprunteur.nom} ({etat})"

""" Nous ne mettons pas ces champs directement dans auteur car
biographie peut faire plusieurs paragraphes de texte et est donc 
un champ lourd qu'on a besoin de charger que sur la page dédiée à l'auteur
et non quand on liste des livres. 
Ce découplage a un intérêt réel dans la séparation entre un utilisateur et son profil"""
class FicheAuteur(models.Model):
    biographie = models.TextField(blank=True)
    site_web = models.URLField(blank=True)
    auteur = models.OneToOneField(Auteur, on_delete=models.CASCADE)