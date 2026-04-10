from django.db import models


TIPO_CHOICE = (
    ("CACHORRO", "CACHORRO"),
    ("GATO", "GATO")
)


class Animal(models.Model):
    tipo = models.CharField(choices=TIPO_CHOICE)
    nome = models.CharField()
    genero = models.CharField()
    idade = models.IntegerField()
    castrado = models.BooleanField()

    def __str__(self):
        return self.nome