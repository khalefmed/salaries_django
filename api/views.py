from rest_framework import generics

from api.permissions import *
from .models import *
from .serializers import *

from rest_framework.decorators import api_view, permission_classes
from django.utils.crypto import get_random_string

from django.http import HttpRequest
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from rest_framework.pagination import PageNumberPagination

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from django.db.models import Q, Avg, Sum, Count

class EtablissementListCreate(generics.ListCreateAPIView):
    queryset = Etablissement.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return EtablissementSerializer
        return EtablissementCustomSerializer
    
    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset().annotate(mean_salary=Avg('etablissement__salaire'))
        liste = self.get_serializer(queryset, many=True).data

        statistiques = Salarie.objects.aggregate(
            moyenne_salaires=Avg('salaire'),
            nombre_salaries=Count('salaire'),
        )

        statistiques['total'] = len(liste)

        

        response_data = {
            'statistiques': statistiques,
            'liste': liste
        }
        return Response(response_data, status=200)

@api_view(['GET'])
def rechercher_etablissement(request):
    valeur = request.query_params.get('valeur', None)
    try:
        if valeur != "":
            etablissements = Etablissement.objects.filter(Q(nom_etablissement__icontains=valeur) | Q(code_etablissement__icontains=valeur))
            etablissements = EtablissementSerializer(etablissements, many=True).data
            return Response(etablissements)
        else :
            etablissements = Etablissement.objects.all()
            etablissements = EtablissementSerializer(etablissements, many=True).data
            return Response(etablissements)


    except Exception as e:
        return Response({
            "erreur": f"{e}"
        }, status=500)

class EtablissementRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return EtablissementSerializer
        return EtablissementCustomSerializer

# Banque Views
class BanqueListCreate(generics.ListCreateAPIView):
    queryset = Banque.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return BanqueSerializer
        return BanqueCustomSerializer

    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        liste = self.get_serializer(queryset, many=True).data

        statistiques = Salarie.objects.filter().aggregate(
            moyenne_salaires=Avg('salaire'),
        )
        statistiques['nombre_comptes'] = Salarie.objects.count()
        statistiques['total'] = len(liste)
        response_data = {
            'statistiques': statistiques,
            'liste': liste
        }
        return Response(response_data, status=200)

@api_view(['GET'])
def rechercher_banque(request):
    valeur = request.query_params.get('valeur', None)
    try:
        if valeur != "":
            banques = Banque.objects.filter(Q(nom_banque__icontains=valeur) | Q(code_banque__icontains=valeur))
            banques = BanqueSerializer(banques, many=True).data
            return Response(banques)
        else :
            banques = Banque.objects.all()
            banques = BanqueSerializer(banques, many=True).data
            return Response(banques)


    except Exception as e:
        return Response({
            "erreur": f"{e}"
        }, status=500)

class BanqueRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Banque.objects.all()
    serializer_class = BanqueSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BanqueSerializer
        return BanqueCustomSerializer



# Salarie Views
class SalarieListCreate(generics.ListCreateAPIView):
    queryset = Salarie.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return SalarieSerializer
        return SalarieCustomSerializer

    def get(self, request, *args, **kwargs):
        utilisateur = request.user

        queryset = Salarie.objects.filter(etablissement=utilisateur.etablissement)
        liste = self.get_serializer(queryset, many=True).data

        statistiques = Salarie.objects.filter(etablissement=utilisateur.etablissement).aggregate(
            moyenne_salaires=Avg('salaire'),
            total_salaires=Sum('salaire'),
        )
        statistiques['total'] = len(liste)
        response_data = {
            'statistiques': statistiques,
            'liste': liste
        }
        return Response(response_data, status=200)

@api_view(['GET'])
def rechercher_salarie(request):
    valeur = request.query_params.get('valeur', None)
    utilisateur = request.user
    try:
        if valeur != "":
            salaries = Salarie.objects.filter(Q(Q(nom_salarie__icontains=valeur) | Q(nni__icontains=valeur), etablissement=utilisateur.etablissement))
            salaries = SalarieCustomSerializer(salaries, many=True).data
            return Response(salaries)
        else :
            salaries = Salarie.objects.filter(etablissement=utilisateur.etablissement)
            salaries = SalarieCustomSerializer(salaries, many=True).data
            return Response(salaries)


    except Exception as e:
        return Response({
            "erreur": f"{e}"
        }, status=500)


class SalarieRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salarie.objects.all()
    serializer_class = SalarieSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SalarieSerializer
        return SalarieCustomSerializer

# Cheque Views
class ChequeListCreate(generics.ListCreateAPIView):
    queryset = Cheque.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return ChequeSerializer
        return ChequeCustomSerializer

    def get(self, request, *args, **kwargs):
        utilisateur = request.user

        
        queryset = Cheque.objects.all()

        liste = self.get_serializer(queryset, many=True).data

        statistiques = {}
    
        
        statistiques['total'] = len(liste)
        statistiques['nombre_comptes'] = Salarie.objects.count()
        
        

        for cheque in liste :
            montant = Etat.objects.aggregate(montant=Sum('montant_net')) 
            if montant['montant'] :
                montant = montant['montant']
            else :
                montant = 0
            cheque['montant'] = montant
        
        montant_total = 0
        for l in liste:
            montant_total += l['montant']
        
        statistiques['moyenne'] = 0
        if (montant_total > len(liste)):
            statistiques['moyenne'] = montant_total / len(liste)

        response_data = {
            'statistiques': statistiques,
            'liste': liste
        }
        return Response(response_data, status=200)

@api_view(['GET'])
def rechercher_cheque(request):
    valeur = request.query_params.get('valeur', None)
    utilisateur = request.user
    try:
        if valeur != "":
            cheques = Cheque.objects.filter(Q(nom_cheque__icontains=valeur) | Q(numero_cheque__icontains=valeur))
            cheques = ChequeCustomSerializer(cheques, many=True).data
            for cheque in cheques :
                montant = Etat.objects.aggregate(montant=Sum('montant_net')) 
                if montant['montant'] :
                    montant = montant['montant']
                else :
                    montant = 0
                cheque['montant'] = montant

            return Response(cheques)
        else :
            cheques = Cheque.objects.all()
            cheques = ChequeCustomSerializer(cheques, many=True).data
            for cheque in cheques :
                montant = Etat.objects.aggregate(montant=Sum('montant_net')) 
                if montant['montant'] :
                    montant = montant['montant']
                else :
                    montant = 0
                cheque['montant'] = montant
            return Response(cheques)


    except Exception as e:
        return Response({
            "erreur": f"{e}"
        }, status=500)

class ChequeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cheque.objects.all()
    serializer_class = ChequeSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ChequeSerializer
        return ChequeCustomSerializer

# Etat Views
class EtatListCreate(generics.ListCreateAPIView):
    queryset = Etat.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return EtatSerializer
        return EtatCustomSerializer



class EtatRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Etat.objects.all()
    serializer_class = EtatSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return EtatSerializer
        return EtatCustomSerializer

# Utilisateur Views
class UtilisateurListCreate(generics.ListCreateAPIView):
    queryset = Utilisateur.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return UtilisateurSerializer
        return UtilisateurCustomSerializer
    
    def get(self, request, *args, **kwargs):

        queryset = Utilisateur.objects.all()
        liste = self.get_serializer(queryset, many=True).data

        statistiques = {}

        statistiques['agents_tresor'] = Utilisateur.objects.filter(etablissement__isnull=True).count()
        statistiques['agents_etablissement'] = Utilisateur.objects.filter(etablissement__isnull=False).count()
        statistiques['total'] = len(liste)
        response_data = {
            'statistiques': statistiques,
            'liste': liste
        }
        return Response(response_data, status=200)
    

@api_view(['GET'])
def rechercher_utilisateur(request):
    valeur = request.query_params.get('valeur', None)
    utilisateur = request.user
    try:
        if valeur != "":
            utilisateurs= Utilisateur.objects.filter(Q(first_name__icontains=valeur) | Q(last_name__icontains=valeur) | Q(telephone__icontains=valeur) | Q(username__icontains=valeur))
            utilisateurs = UtilisateurCustomSerializer(utilisateurs, many=True).data
            return Response(utilisateurs)
        else :
            utilisateurs = Utilisateur.objects.all()
            utilisateurs = UtilisateurCustomSerializer(utilisateurs, many=True).data
            return Response(utilisateurs)


    except Exception as e:
        print(e)
        return Response({
            "erreur": f"{e}"
        }, status=500)

class UtilisateurRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UtilisateurSerializer
        return UtilisateurCustomSerializer
    
class RegisterView(APIView):
    def post(self, request):
        serializer = UtilisateurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        telephone = request.data['telephone']
        Utilisateur = Utilisateur.objects.get(telephone=telephone)
        refresh = RefreshToken.for_Utilisateur(Utilisateur)
        
        return Response({
            "message" : "Utilisateur créé avec succès",
            "token" : str(refresh.access_token)
        })
    

class SeConnecter(TokenObtainPairView):
    serializer_class = ConnexionSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        telephone = serializer.validated_data['telephone']
        mot_de_passe = serializer.validated_data['mot_de_passe']

        utilisateur = Utilisateur.objects.filter(telephone=telephone).first()

        if utilisateur:

            utilisateur = authenticate(request, telephone=telephone, password=mot_de_passe)
            if utilisateur :
                
                refresh = RefreshToken.for_user(utilisateur)
                role = "Agent Trésor"
                if utilisateur.etablissement:
                    role = f"Agent {utilisateur.etablissement.code_etablissement}"
                
                if utilisateur.is_staff :
                    role = "Administrateur"
                
                utilisateur = UtilisateurSerializer(utilisateur).data
                data = {
                    'token': str(refresh.access_token),
                    'utilisateur' : utilisateur,
                    'role' : role
                }
                
                return Response(data, status=status.HTTP_200_OK)
            
            else :
                return Response( status=401)

        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Utilisateur_profil(request):
    Utilisateur = request.user
    try:
        Utilisateur = UtilisateurSerializer(Utilisateur)
        return JsonResponse(Utilisateur.data)
    except Exception as e:
        return JsonResponse({
            "status": 500,
            "message": f"Failed to load Utilisateurs profile {e}"
        })


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_mot_de_passe(request):
    Utilisateur = request.user
    try:
        data = json.loads(request.body.decode('utf-8'))
        ancien = data.get('ancien', {})
        nouveau = data.get('nouveau', {})

        if check_password(ancien, Utilisateur.password):
            Utilisateur.password = make_password(nouveau)
            Utilisateur.save()

            return Response({"message" : "Mot de passe modifié avec succés"}, status=status.HTTP_200_OK)
        else:
            return Response({"message" : "Mot de passe incorrecte"}, status=400)

    except Exception as e:
        return Response({"message" : "Une erreur est survenue"}, status=500)


