from django import forms
from .models import Animal, Adotante


class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['tipo', 'nome', 'genero', 'idade', 'castrado']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do animal'}),
            'genero': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masculino / Feminino'}),
            'idade': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'castrado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AdotanteForm(forms.ModelForm):
    class Meta:
        model = Adotante
        fields = ['nome', 'email', 'telefone', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
