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

        statistiques = Salarie.objects.aggregate(
            moyenne_salaires=Avg('salaire'),
            nombre_salaries=Count('salaire')
        )

        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'statistiques': statistiques,
            'liste': serializer.data
        }
        return Response(response_data, status=200)

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

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return ChequeSerializer
        return ChequeCustomSerializer

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

        Utilisateur = Utilisateur.objects.filter(telephone=telephone).first()

        if Utilisateur:
            Utilisateur = authenticate(request, telephone=telephone, password=mot_de_passe)
            refresh = RefreshToken.for_user(Utilisateur)
            data = {
                'token': str(refresh.access_token),
                'user' : Utilisateur
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message" : "Données invalides"}, status=status.HTTP_401_UNAUTHORIZED)


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


@api_view(['POST'])
def token_verify(request):
    token = request.data.get('token')

    if not token:
        return Response({'error': 'Le token est requis'}, status=status.HTTP_400_BAD_REQUEST)

    if not token.startswith('Bearer '):
        return Response({'error': 'Le format du token  est invalide'}, status=status.HTTP_400_BAD_REQUEST)

    token = token.split(' ')[1]

    try:
        refresh = RefreshToken(token)
        refresh.verify()
    except TokenError as e:
        if "Token has expired" in str(e):
            return Response({'error': 'Le token a expiré'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({'detail': 'Le token est valide'}, status=status.HTTP_200_OK)

