from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from api.models import *

# Register your models here.



admin.site.register(Utilisateur)
admin.site.register(Etablissement)
admin.site.register(Banque)
admin.site.register(Salarie)
admin.site.register(Cheque)
admin.site.register(Etat)
admin.site.register(EtatSalarie)
