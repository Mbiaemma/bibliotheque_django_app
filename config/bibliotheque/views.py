from operator import contains

from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from .models import *
import json


# Create your views here.
def liste_livres(request):
    lignes = []
    for livre in Livre.objects.all():
        url = reverse("detail-livre", args=[livre.isbn])
        lignes.append(f'<li><a href="{url}">{livre.titre}</a></li>')
    html = "<ul>" + "".join(lignes) + "</ul>"
    return HttpResponse(html)


def detail_livre(request, isbn):
    try :
        livre = Livre.objects.get(isbn=isbn)
    except Livre.DoesNotExist:
        raise Http404("Aucun livre ne correspond à cet isbn.")
    return HttpResponse(livre.titre)

def ajouter_livre(request):
    if request.method == "POST":
        return HttpResponse("Formulaire reçu")
    elif request.method == "GET":
        return HttpResponse("Nouveau formulaire")
    else:
        return HttpResponse("Méthode non prise en charge")

def livres_json(request):
    data = [
        {"titre" : livre.titre, "isbn" : livre.isbn}
        for livre in Livre.objects.all()
    ]
    data = json.dumps(data)
    return HttpResponse(data)

def ajouter_commentaire(request):
    """ request.POST n'est pas un booléen mais un dictionnaire des champs fournis (QueryDict).
    Un dictionnaire vide est faux en python donc request.POST sera évalué à false alors que la requête
    est bel et bien un POST."""
    if request.method == "POST":
        # traitement du commentaire
        return HttpResponse("Commentaire ajoute")
    return HttpResponse("Formulaire vide")


# class ListeLivres(View):
    def get(self, request):
        lignes = []
        for livre in Livre.objects.all():
            url = reverse("detail-livre", args=[livre.isbn])
            lignes.append(f'<li><a href="{url}">{livre.titre}</a></li>')
        html = "<ul>" + "".join(lignes) + "</ul>"
        return HttpResponse(html)


# Django cherche sans qu'on ai à lui préciser le template
class ListeLivres(ListView):
    model = Livre
    context_object_name = "livres" #Renommage de la variable de contexte
    ordering = ["titre"]  #Trie des livres par défaut

class LivresParGenre(ListView):
    template_name = "bibliotheque/livres_par_genre.html"

    def get_queryset(self):
        return Livre.objects.filter(genres__nom=self.kwargs["nom"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["genre_nom"] = self.kwargs["nom"]
        context["nombre_livres"] = context["livre_list"].count()
        return context

""" Avec DetailView, la gestion du livre introuvable n'est plus 
de notre responsabilité : get_object() fait en interne l'équivalent
de get_object_or_404() et lève Http404 automatiquement si aucune
ligne ne correspond """
class DetailLivre(DetailView):
    model = Livre
    template_name = "bibliotheque/livre_detail.html"
    slug_field = "isbn"
    slug_url_kwarg = "isbn"

""" En ce qui concerne FBV et CBV, on peut dire qu'on préférera utiliser
les vues génériques(CBV) lorsque la vue couvre les cas les plus fréquent, quand
le besoin correspond à un schéma exemple de l'exercice 17. Par contre on utilisera
les vues fonctionnelles quand la logique devient un enchainement d'étapes qui ne
correspond à aucun schéma exemple de l'exercice 9"""