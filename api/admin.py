from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import *

# Register your models here.



from django.contrib import admin
from .models import Etablissement, Banque, Salarie, Etat, Cheque, EtatSalarie, Utilisateur

class EtablissementAdmin(admin.ModelAdmin):
    list_display = ("nom_etablissement", "code_etablissement", "url_fichier")

class BanqueAdmin(admin.ModelAdmin):
    list_display = ("nom_banque", "code_banque")

class SalarieAdmin(admin.ModelAdmin):
    list_display = ("nom_salarie", "nni", "etat_salarie", "salaire", "numero_compte", "banque", "etablissement")

class EtatAdmin(admin.ModelAdmin):
    list_display = ("nom_etat", "date_etat", "etablissement")

class ChequeAdmin(admin.ModelAdmin):
    list_display = ("numero_cheque", "nom_cheque", "etat")

class EtatSalarieAdmin(admin.ModelAdmin):
    list_display = ("montant_net", "salarie", "etat")

class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ("username", "telephone", "etablissement", "is_staff", "is_active", "date_joined")


admin.site.site_header = "Systeme salaires"

admin.site.register(Etablissement, EtablissementAdmin)
admin.site.register(Banque, BanqueAdmin)
admin.site.register(Salarie, SalarieAdmin)
admin.site.register(Etat, EtatAdmin)
admin.site.register(Cheque, ChequeAdmin)
admin.site.register(EtatSalarie, EtatSalarieAdmin)
admin.site.register(Utilisateur, UtilisateurAdmin)

