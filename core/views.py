from django.shortcuts import render, redirect
from .models import Animal, Adotante
from .forms import AnimalForm, AdotanteForm


def home(request):
    return render(request, 'home.html')


def animal_list(request):
    animais = Animal.objects.all().order_by('tipo', 'nome')
    return render(request, 'animal_list.html', {'animais': animais})


def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:animal_list')
    else:
        form = AnimalForm()
    return render(request, 'animal_form.html', {'form': form})


def contact(request):
    return render(request, 'contact.html')


def adotante_list(request):
    adotantes = Adotante.objects.all().order_by('-criado_em')
    return render(request, 'adotante_list.html', {'adotantes': adotantes})


def adotante_create(request):
    if request.method == 'POST':
        form = AdotanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:adotante_list')
    else:
        form = AdotanteForm()
    return render(request, 'adotante_form.html', {'form': form})
