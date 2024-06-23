
from django.urls import path
from .views import *


urlpatterns = [

    # Etablissement URLs
    path('etablissements/', EtablissementListCreate.as_view(), name='etablissement-list-create'),
    path('etablissements/<int:pk>/', EtablissementRetrieveUpdateDestroy.as_view(), name='etablissement-detail'),
    path('recherche/etablissements/', rechercher_etablissement, name='recherche-etablissement'),

    # Banque URLs
    path('banques/', BanqueListCreate.as_view(), name='banque-list-create'),
    path('banques/<int:pk>/', BanqueRetrieveUpdateDestroy.as_view(), name='banque-detail'),
    path('recherche/banques/', rechercher_banque, name='recherche-banque'),

    # Salarie URLs
    path('salaries/', SalarieListCreate.as_view(), name='salarie-list-create'),
    path('salaries/<int:pk>/', SalarieRetrieveUpdateDestroy.as_view(), name='salarie-detail'),
    path('recherche/salaries/', rechercher_salarie, name='recherche-salarie'),

    # Cheque URLs
    path('cheques/', ChequeListCreate.as_view(), name='cheque-list-create'),
    path('cheques/<int:pk>/', ChequeRetrieveUpdateDestroy.as_view(), name='cheque-detail'),
    path('recherche/cheques/', rechercher_cheque, name='recherche-cheque'),

    # Etat URLs
    path('etats/', EtatListCreate.as_view(), name='etat-list-create'),
    path('etats/<int:pk>/', EtatRetrieveUpdateDestroy.as_view(), name='etat-detail'),

    # User URLs
    path('utilisateurs/', UtilisateurListCreate.as_view(), name='user-list-create'),
    path('utilisateurs/<int:pk>/', UtilisateurRetrieveUpdateDestroy.as_view(), name='user-detail'),
    path('recherche/utilisateurs/', rechercher_utilisateur, name='recherche-utilisateur'),

    path('connexion/', SeConnecter.as_view(), name='connexion'),
    path('profil/', Utilisateur_profil, name='profile-view'),
    path('modifier_mot_de_passe/', modifier_mot_de_passe, name='update-password'),
]
