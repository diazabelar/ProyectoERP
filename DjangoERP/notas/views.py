from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Categoria, Nota
from django.contrib import messages

@login_required
def index(request):
    notas = Nota.objects.filter(usuario=request.user, archivado=False).order_by('-fecha_actualizacion')
    return render(request, 'notas/index.html', {
        'title': 'Mis Notas',
        'notas': notas,
    })

@login_required
def categorias_list(request):
    categorias = Categoria.objects.filter(usuario=request.user)
    return render(request, 'notas/categorias_list.html', {
        'title': 'Categorías',
        'categorias': categorias,
    })

@login_required
def categoria_create(request):
    # Aquí iría la lógica para crear una categoría
    return render(request, 'notas/categoria_form.html', {
        'title': 'Nueva Categoría',
    })

@login_required
def nota_create(request):
    # Aquí iría la lógica para crear una nota
    return render(request, 'notas/nota_form.html', {
        'title': 'Nueva Nota',
    })

@login_required
def nota_detail(request, pk):
    nota = get_object_or_404(Nota, pk=pk, usuario=request.user)
    return render(request, 'notas/nota_detail.html', {
        'title': nota.titulo,
        'nota': nota,
    })

@login_required
def nota_edit(request, pk):
    nota = get_object_or_404(Nota, pk=pk, usuario=request.user)
    # Aquí iría la lógica para editar una nota
    return render(request, 'notas/nota_form.html', {
        'title': f'Editar: {nota.titulo}',
        'nota': nota,
    })
