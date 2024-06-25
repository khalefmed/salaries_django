from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Etablissement, Banque, Salarie, Cheque, Etat, Utilisateur, EtatSalarie

Utilisateur = get_user_model()

class ConnexionSerializer(serializers.Serializer):
    telephone = serializers.CharField()
    mot_de_passe = serializers.CharField(write_only=True)

class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = '__all__'


class SalarieSerializer(serializers.ModelSerializer):
    etablissement = serializers.PrimaryKeyRelatedField(queryset=Etablissement.objects.all(), required=False)
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
    cheque = ChequeSerializer()
    etablissement = EtablissementSerializer()

    class Meta:
        model = Etat
        fields = '__all__'

class EtatSalarieCustomSerializer(serializers.ModelSerializer):
    salarie = SalarieSerializer()
    etat = EtatSerializer()

    class Meta:
        model = EtatSalarie
        fields = '__all__'

class UtilisateurCustomSerializer(serializers.ModelSerializer):
    etablissement = EtablissementSerializer()

    class Meta:
        model = Utilisateur
        fields = '__all__'
