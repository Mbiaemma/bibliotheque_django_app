from django.urls import path, register_converter
from . import views, converters

register_converter(converters.ISBNConverter, "isbn")

urlpatterns = [
    path('ouvrages/', views.liste_livres, name='liste_livres'),
    # path("livres/nouveautes/", views.nouveautes, name="nouveautes"), #N'affichait jamais le résultat attendu car passait après detail-livre or une requête vers cette url correspondait d'abord à une requête vers 'livres/<str:isbn>/' avec isbn = "nouveautes"
    # path('livres/<str:isbn>/', views.detail_livre, name="detail-livre"), #Car un isbn a pour format xxx-x-xxxx-xxxx-x par exemple (isbn 13) ou les x sont les 13 chiffres du isbn un convertisseur int ne peut pas capturer les tirets
    # path('livres/<isbn:isbn>/', views.detail_livre, name="detail-livre"),
    path('livres_json/', views.livres_json, name="livres_json"),
    # path('livres/', views.ListeLivres.as_view()),
    path('livres/', views.ListeLivres.as_view()),
    path( "genres/<str:nom>/", views.LivresParGenre.as_view()),
    path('livres/<isbn:isbn>/', views.DetailLivre.as_view(), name="detail-livre"),
]
