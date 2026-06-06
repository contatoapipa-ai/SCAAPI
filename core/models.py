from django.db import models
from io import BytesIO
from django.core.files.base import ContentFile

try:
    from PIL import Image
except Exception:
    Image = None


def _resize_image_field(image_field):
    if not image_field or Image is None:
        return
    try:
        img = Image.open(image_field.path)
    except Exception:
        try:
            image_field.open()
            img = Image.open(image_field)
        except Exception:
            return

    max_size = (800, 800)
    try:
        resample_filter = Image.Resampling.LANCZOS
    except Exception:
        resample_filter = getattr(Image, 'LANCZOS', Image.BICUBIC)
    img.thumbnail(max_size, resample_filter)

    buffer = BytesIO()
    fmt = 'JPEG' if img.mode in ('RGB', 'L', 'P') else 'PNG'
    if img.mode in ('RGBA', 'LA') and fmt == 'JPEG':
        background = Image.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background
        fmt = 'JPEG'
    img.save(buffer, format=fmt, quality=85)
    filecontent = ContentFile(buffer.getvalue())
    name = image_field.name
    image_field.save(name, filecontent, save=False)
    buffer.close()


ESPECIE_CHOICE = (
    ("CACHORRO", "Cachorro"),
    ("GATO", "Gato"),
)

SEXO_CHOICE = (
    ("MACHO", "Macho"),
    ("FEMEA", "Fêmea"),
)

RACA_CHOICE = (
    ("SRD", "SRD (Sem Raça Definida)"),
    ("POODLE", "Poodle"),
    ("LABRADOR", "Labrador"),
    ("BULLDOG", "Bulldog"),
    ("SHIH-TZU", "Shih-Tzu"),
    ("SIAMES", "Siamês"),
    ("PERSA", "Persa"),
    ("MAINE-COON", "Maine Coon"),
    ("OUTRO", "Outro"),
)

PELAGEM_CHOICE = (
    ("CURTA", "Pelagem Curta"),
    ("MEDIA", "Pelagem Média"),
    ("LONGA", "Pelagem Longa"),
    ("AUSENTE", "Sem Pelagem"),
)

STATUS_CHOICE = (
    ("VIVO", "Vivo"),
    ("MORTO", "Morto"),
)

ESTERILIZACAO_CHOICE = (
    ("SIM", "Sim"),
    ("NAO", "Não"),
)


class Animal(models.Model):
    especie = models.CharField('espécie', max_length=20, choices=ESPECIE_CHOICE, default="CACHORRO")
    nome = models.CharField('nome', max_length=80)
    foto = models.ImageField('foto', upload_to='animals/', null=True, blank=True)
    sexo = models.CharField('sexo', max_length=20, choices=SEXO_CHOICE, default="MACHO")
    esterilizacao = models.CharField('esterilização', max_length=20, choices=ESTERILIZACAO_CHOICE, default="NAO")
    nascimento = models.DateField('data de nascimento', null=True, blank=True)
    raca = models.CharField('raça', max_length=80, choices=RACA_CHOICE, default="SRD")
    pelagem = models.CharField('pelagem', max_length=20, choices=PELAGEM_CHOICE, default="CURTA")
    status = models.CharField('status', max_length=20, choices=STATUS_CHOICE, default="VIVO")
    adotado = models.BooleanField('adotado', default=False)
    adotante = models.ForeignKey('core.Adotante', on_delete=models.SET_NULL, null=True, blank=True, related_name='animais')

    def __str__(self):
        return f"{self.nome} ({self.especie})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        _resize_image_field(self.foto)
        if self.foto:
            super().save(update_fields=['foto'])


class AnimalImage(models.Model):
    animal = models.ForeignKey('core.Animal', on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField('imagem', upload_to='animal_images/')
    criado_em = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        verbose_name = 'Imagem do Animal'
        verbose_name_plural = 'Imagens do Animal'

    def __str__(self):
        return f"Imagem de {self.animal.nome}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        _resize_image_field(self.imagem)
        if self.imagem:
            super().save(update_fields=['imagem'])


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
