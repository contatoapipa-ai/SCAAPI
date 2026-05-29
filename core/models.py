from django.db import models


TIPO_CHOICE = (
    ("CACHORRO", "CACHORRO"),
    ("GATO", "GATO")
)


class Animal(models.Model):
    tipo = models.CharField('tipo de animal', max_length=20, choices=TIPO_CHOICE)
    nome = models.CharField('nome', max_length=80)
    genero = models.CharField('gênero', max_length=20)
    idade = models.IntegerField('idade em anos')
    castrado = models.BooleanField('castrado')

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Adotante(models.Model):
    nome = models.CharField('nome', max_length=120)
    email = models.EmailField('email', blank=True)
    telefone = models.CharField('telefone', max_length=30, blank=True)
    endereco = models.TextField('endereço', blank=True)
    criado_em = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Adotante'
        verbose_name_plural = 'Adotantes'

    def __str__(self):
        return self.nome
