from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from datetime import date


class Etablissement(models.Model):
    nom_etablissement = models.CharField(max_length=50)
    code_etablissement = models.CharField(max_length=50)
    url_fichier = models.CharField(max_length=150)

    def __str__(self):
        return str(self.code_etablissement)
    
class Banque(models.Model):
    nom_banque = models.CharField(max_length=50)
    code_banque = models.CharField(max_length=50)

    def __str__(self):
        return str(self.code_banque)
    
class Salarie(models.Model):
    nom_salarie = models.CharField(max_length=50)
    nni = models.IntegerField()
    etat_salarie = models.BooleanField(default=True)
    salaire = models.DecimalField(max_digits=15, decimal_places=2)
    numero_compte = models.IntegerField()
    banque = models.ForeignKey(Banque, related_name='banque', on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Etablissement, related_name='etablissement', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nom_salarie)
    
class Cheque(models.Model):
    numero_cheque = models.IntegerField()
    nom_cheque = models.CharField(max_length=50)
    etablissement = models.ForeignKey(Etablissement, related_name='cheque_etablissement', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.nom_cheque)


class Etat(models.Model):
    nom_etat = models.CharField(max_length=50, default="Etat")
    date_etat = models.DateField(default=date.today)
    cheque = models.ForeignKey(Cheque, related_name='cheque', on_delete=models.CASCADE)
    etablissement = models.ForeignKey(Etablissement, related_name='etat_etablissement', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return str(self.nom_etat)
    
class EtatSalarie(models.Model):
    montant_net = models.DecimalField(max_digits=15, decimal_places=2)
    salarie = models.ForeignKey(Salarie, related_name='salarie', on_delete=models.CASCADE)
    etat = models.ForeignKey(Etat, related_name='etat', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.salarie)




class Utilisateur(AbstractUser):
    telephone = models.CharField(max_length=8, unique=True)
    etablissement = models.ForeignKey(Etablissement, related_name='cheque', on_delete=models.CASCADE, null=True, blank=True)

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

