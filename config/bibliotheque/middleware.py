import time
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.http import HttpResponseForbidden


def journalisation_middleware(get_response):
    def middleware(request):
        print("Début Journalisation")
        print(f"{request.method} {request.path}")
        response = get_response(request)
        print("Fin Journalisation")
        return response
    return middleware

def chrono_middleware(get_response):
    """
    L’exception est levée lorsqu’un middleware n’est pas utilisé dans la configuration serveur.
    """
    if not getattr(settings, "ACTIVER_CHRONO", False):
        raise MiddlewareNotUsed("ACTIVER_CHRONO n'est pas activé dans settings.")
    def middleware(request):
        print("Début Chronométrage")
        debut = time.perf_counter()
        response = get_response(request)
        duree = (time.perf_counter() - debut) * 1000
        print(f"{request.path} traité en {duree:.1f} ms")
        print("Fin Chronométrage")
        return response
    return middleware

""" Lorsque le middleware de journalisation vient avant celui de chronométrage
on a en sorti
Début Journalisation
GET /bibliotheque/livres/
Début Chronométrage
/bibliotheque/livres/ traité en 14.5 ms
Fin Chronométrage
Fin Journalisation 
La journalisation se déclanche puis avant qu'elle ne prenne fin
le chronométrage se lance et prend fin

Lorsque le middleware de journalisation vient après on a
Début Chronométrage
Début Journalisation
GET /bibliotheque/livres/
Fin Journalisation
/bibliotheque/livres/ traité en 2.3 ms
Fin Chronométrage
Le chronométrage se lance puis la journalisation la journalisation s'execute
et prend fin avant que le chronométrage ne s'exécute et prenne fin.

- Le chrono dans le cas 1 ne mesurait que le temps d'exécution de la vue car c'était la 
couche la plus proche d'elle.
- Dans le cas 2 le chrono mesure en plus du temps de la vue le temps d'exécution de la journalisation
La requête traverse la pile de middleware de haut en bas dans l'ordre jusqu'à la vue
et la réponse la traverse ensuite de bas en haut dans l'ordre inverse """


def autorisation_middleware(get_response):
    def middleware(request):
        if request.path.startswith("/bibliotheque/livres/") and "X-Client-Autorise" not in request.headers:
            return HttpResponseForbidden("En-tête manquant.")
        return get_response(request)
    return middleware


""" Pour la reflexion de l'exercice 24 on peut dire que c'est un travail de middleware 
car le faire dans une vue implique de devoir l'appeler dans chaque vue sans exception
alors qu'avec un middleware, il s'exécutera sur toute requête qui traverse la pile de middleware."""