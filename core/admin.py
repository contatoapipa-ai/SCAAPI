from django.contrib import admin
from .models import Animal, Adotante


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ["tipo", "nome", "idade", "genero", "castrado"]


@admin.register(Adotante)
class AdotanteAdmin(admin.ModelAdmin):
    list_display = ["nome", "email", "telefone", "criado_em"]
    readonly_fields = ["criado_em"]