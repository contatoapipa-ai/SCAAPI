from django.shortcuts import render, redirect
from .models import Animal, Adotante, AnimalImage
from django.db import models
from .forms import AnimalForm, AdotanteForm


def home(request):
    return render(request, 'home.html')


def animal_list(request):
    q = request.GET.get('q', '').strip()
    animais = Animal.objects.select_related('adotante').prefetch_related('imagens').all()
    if q:
        animais = animais.filter(models.Q(nome__icontains=q) | models.Q(raca__icontains=q) | models.Q(especie__icontains=q))
    animais = animais.order_by('especie', 'nome')
    return render(request, 'animal_list.html', {'animais': animais, 'q': q})
    


def animal_create(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            animal = form.save()
            for image in form.cleaned_data.get('images', []):
                if image:
                    AnimalImage.objects.create(animal=animal, imagem=image)
            return redirect('core:animal_list')
    else:
        form = AnimalForm()
    return render(request, 'animal_form.html', {'form': form})


def animal_edit(request, pk):
    animal = Animal.objects.get(pk=pk)
    if request.method == 'POST':
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            animal = form.save()
            for image in form.cleaned_data.get('images', []):
                if image:
                    AnimalImage.objects.create(animal=animal, imagem=image)
            return redirect('core:animal_list')
    else:
        form = AnimalForm(instance=animal)
    return render(request, 'animal_form.html', {'form': form, 'animal': animal})


def animal_delete(request, pk):
    animal = Animal.objects.get(pk=pk)
    if request.method == 'POST':
        animal.delete()
        return redirect('core:animal_list')
    return render(request, 'animal_confirm_delete.html', {'animal': animal})


def contact(request):
    return render(request, 'contact.html')


def adotante_list(request):
    q = request.GET.get('q', '').strip()
    adotantes = Adotante.objects.all()
    if q:
        adotantes = adotantes.filter(models.Q(nome__icontains=q) | models.Q(email__icontains=q) | models.Q(telefone__icontains=q))
    adotantes = adotantes.order_by('-criado_em')
    return render(request, 'adotante_list.html', {'adotantes': adotantes, 'q': q})


def adotante_create(request):
    if request.method == 'POST':
        form = AdotanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:adotante_list')
    else:
        form = AdotanteForm()
    return render(request, 'adotante_form.html', {'form': form})


def adotante_edit(request, pk):
    adotante = Adotante.objects.get(pk=pk)
    if request.method == 'POST':
        form = AdotanteForm(request.POST, instance=adotante)
        if form.is_valid():
            form.save()
            return redirect('core:adotante_list')
    else:
        form = AdotanteForm(instance=adotante)
    return render(request, 'adotante_form.html', {'form': form, 'adotante': adotante})


def adotante_delete(request, pk):
    adotante = Adotante.objects.get(pk=pk)
    if request.method == 'POST':
        adotante.delete()
        return redirect('core:adotante_list')
    return render(request, 'adotante_confirm_delete.html', {'adotante': adotante})
