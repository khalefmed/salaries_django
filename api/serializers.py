from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Etablissement, Banque, Salarie, Cheque, Etat

Utilisateur = get_user_model()

class ConnexionSerializer(serializers.Serializer):
    telephone = serializers.CharField()
    password = serializers.CharField(write_only=True)

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = '__all__'


class SalarieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salarie
        fields = '__all__'


class BanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banque
        fields = '__all__'


class ChequeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = '__all__'


class EtatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etat
        fields = '__all__'


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'

class EtablissementCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = '__all__'


class BanqueCustomSerializer(serializers.ModelSerializer):
    salaries = SalarieSerializer(many=True, read_only=True)

    class Meta:
        model = Banque
        fields = '__all__'


# Salarie Serializers


class SalarieCustomSerializer(serializers.ModelSerializer):
    banque = BanqueSerializer()
    etablissement = EtablissementSerializer()

    class Meta:
        model = Salarie
        fields = '__all__'


class ChequeCustomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cheque
        fields = '__all__'



class EtatCustomSerializer(serializers.ModelSerializer):
    salarie = SalarieSerializer()
    cheque = ChequeSerializer()

    class Meta:
        model = Etat
        fields = '__all__'

class UtilisateurCustomSerializer(serializers.ModelSerializer):
    etablissement = EtablissementSerializer()

    class Meta:
        model = Utilisateur
        fields = '__all__'
