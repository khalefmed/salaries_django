
from django.urls import path
from .views import *


urlpatterns = [

    # Etablissement URLs
    path('etablissements/', EtablissementListCreate.as_view(), name='etablissement-list-create'),
    path('etablissements/<int:pk>/', EtablissementRetrieveUpdateDestroy.as_view(), name='etablissement-detail'),

    # Banque URLs
    path('banques/', BanqueListCreate.as_view(), name='banque-list-create'),
    path('banques/<int:pk>/', BanqueRetrieveUpdateDestroy.as_view(), name='banque-detail'),

    # Salarie URLs
    path('salaries/', SalarieListCreate.as_view(), name='salarie-list-create'),
    path('salaries/<int:pk>/', SalarieRetrieveUpdateDestroy.as_view(), name='salarie-detail'),

    # Cheque URLs
    path('cheques/', ChequeListCreate.as_view(), name='cheque-list-create'),
    path('cheques/<int:pk>/', ChequeRetrieveUpdateDestroy.as_view(), name='cheque-detail'),

    # Etat URLs
    path('etats/', EtatListCreate.as_view(), name='etat-list-create'),
    path('etats/<int:pk>/', EtatRetrieveUpdateDestroy.as_view(), name='etat-detail'),

    # User URLs
    path('users/', UtilisateurListCreate.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UtilisateurRetrieveUpdateDestroy.as_view(), name='user-detail'),

    path('connexion/', SeConnecter.as_view(), name='login-view'),
    path('signup/', RegisterView.as_view(), name='register-view'),
    path('compte/', Utilisateur_profil, name='profile-view'),
    path('modifier_mot_de_passe/', modifier_mot_de_passe, name='update-password'),
]
