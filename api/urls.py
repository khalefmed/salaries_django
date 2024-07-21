
from django.urls import path
from .views import *


urlpatterns = [

    path('acceuil/', acceuil, name='acceuil'),
    path('acceuil/etablissement', acceuil_etablissement, name='acceuil-etablissement'),

    # Etablissement URLs
    path('etablissements/', EtablissementListCreate.as_view(), name='etablissement-list-create'),
    path('etablissements/<int:pk>/', EtablissementRetrieveUpdateDestroy.as_view(), name='etablissement-detail'),
    path('recherche/etablissements/', rechercher_etablissement, name='recherche-etablissement'),
    path('activer_etablissement/<int:id>/', activer_etablissement, name='activer-etablissement'),
    path('desactiver_etablissement/<int:id>/', desactiver_etablissement, name='desactiver-etablissement'),
    path('etablissement_active/', etablissement_active, name='etablissement_active'),

    # Banque URLs
    path('banques/', BanqueListCreate.as_view(), name='banque-list-create'),
    path('banques/<int:pk>/', BanqueRetrieveUpdateDestroy.as_view(), name='banque-detail'),
    path('recherche/banques/', rechercher_banque, name='recherche-banque'),
    path('activer_banque/<int:id>/', activer_banque, name='activer-banque'),
    path('desactiver_banque/<int:id>/', desactiver_banque, name='desactiver-banque'),
    path('banque_active/', banque_active, name='banque_active'),

    # Salarie URLs
    path('salaries/', SalarieListCreate.as_view(), name='salarie-list-create'),
    path('salaries/<int:pk>/', SalarieRetrieveUpdateDestroy.as_view(), name='salarie-detail'),
    path('recherche/salaries/', rechercher_salarie, name='recherche-salarie'),
    path('activer_salarie/<int:id>/', activer_salarie, name='activer-salarie'),
    path('desactiver_salarie/<int:id>/', desactiver_salarie, name='desactiver-salarie'),

    # Cheque URLs
    path('cheques/', ChequeListCreate.as_view(), name='cheque-list-create'),
    path('cheques/<int:pk>/', ChequeRetrieveUpdateDestroy.as_view(), name='cheque-detail'),
    path('cheques_etablissement/', cheque_etablissement, name='cheque-etablissement'),
    path('recherche/cheques/', rechercher_cheque, name='recherche-cheque'),

    # Etat URLs
    path('etats/', EtatListCreate.as_view(), name='etat-list-create'),
    path('creer_etat/', creer_etat, name='creer-etat'),
    path('etats_etablissement/', EtatEtablissementListCreate.as_view(), name='etat-etablissement-list-create'),
    path('etats_salaries/<int:id>', etats_salaries, name='etat-etablissement-list-create'),
    path('etats/<int:pk>/', EtatRetrieveUpdateDestroy.as_view(), name='etat-detail'),
    path('recherche/etats/', rechercher_etat, name='recherche-etat'),
    path('recherche/etats_etablissement/', rechercher_etat_etablissement, name='recherche-etat'),

    # User URLs
    path('utilisateurs/', UtilisateurListCreate.as_view(), name='user-list-create'),
    path('utilisateurs/<int:pk>/', UtilisateurRetrieveUpdateDestroy.as_view(), name='user-detail'),
    path('recherche/utilisateurs/', rechercher_utilisateur, name='recherche-utilisateur'),

    path('connexion/', SeConnecter.as_view(), name='connexion'),
    path('profil/', Utilisateur_profil, name='profile-view'),
    path('modifier_informations/', modifier_informations, name='modifier-informations'),
    path('modifier_mot_de_passe/', modifier_mot_de_passe, name='modifier-mot-passe'),
]
