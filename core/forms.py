from django import forms
from django.db.models import Q
from .models import Animal, Adotante


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    widget = MultiFileInput

    def to_python(self, data):
        if not data:
            return []

        parent = super(MultiFileField, self)

        if isinstance(data, list):
            return [parent.to_python(item) for item in data if item]

        return [parent.to_python(data)]

    def validate(self, data):
        if self.required and not data:
            raise forms.ValidationError(
                self.error_messages['required'],
                code='required'
            )

        parent = super(MultiFileField, self)

        if isinstance(data, list):
            for item in data:
                parent.validate(item)
        else:
            parent.validate(data)


class AnimalForm(forms.ModelForm):
    images = MultiFileField(
        required=False,
        label='Fotos adicionais',
        widget=MultiFileInput(attrs={'class': 'form-control', 'multiple': True})
    )

    class Meta:
        model = Animal
        fields = ['especie', 'nome', 'foto', 'sexo', 'esterilizacao', 'nascimento', 'raca', 'pelagem', 'status', 'adotado']
        widgets = {
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do animal'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'esterilizacao': forms.Select(attrs={'class': 'form-select'}),
            'nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'raca': forms.Select(attrs={'class': 'form-select'}),
            'pelagem': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'adotado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_foto(self):
        foto = self.cleaned_data.get('foto')
        if not foto:
            return foto
        # Validate file size (<= 3MB)
        max_size = 3 * 1024 * 1024
        if foto.size > max_size:
            raise forms.ValidationError('A imagem deve ter no máximo 3 MB.')
        # Validate content type
        content_type = getattr(foto, 'content_type', '')
        allowed = ['image/jpeg', 'image/png']
        if content_type not in allowed:
            raise forms.ValidationError('Formato inválido. Use JPG ou PNG.')
        return foto

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images is None:
            images = self.files.getlist('images')
        if not images:
            return []

        max_size = 3 * 1024 * 1024
        allowed = ['image/jpeg', 'image/png']
        for image in images:
            if image.size > max_size:
                raise forms.ValidationError('Cada imagem deve ter no máximo 3 MB.')
            content_type = getattr(image, 'content_type', '')
            if content_type not in allowed:
                raise forms.ValidationError('Formato inválido. Use JPG ou PNG para todas as imagens.')
        return images


class AdotanteForm(forms.ModelForm):
    animais = forms.ModelMultipleChoiceField(
        queryset=Animal.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'size': 8})
    )

    class Meta:
        model = Adotante
        fields = ['nome', 'email', 'telefone', 'endereco', 'animais']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['animais'].queryset = Animal.objects.filter(Q(adotado=False) | Q(adotante=self.instance))
            self.fields['animais'].initial = self.instance.animais.all()
        else:
            self.fields['animais'].queryset = Animal.objects.filter(adotado=False)

    def save(self, commit=True):
        adotante = super().save(commit=commit)
        selected_animais = self.cleaned_data.get('animais')
        if commit and selected_animais is not None:
            Animal.objects.filter(adotante=adotante).exclude(pk__in=[animal.pk for animal in selected_animais]).update(adotante=None, adotado=False)
            for animal in selected_animais:
                animal.adotante = adotante
                animal.adotado = True
                animal.save(update_fields=['adotante', 'adotado'])
        return adotante
