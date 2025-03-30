from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from .models import HojaCalculo, Celda  # Uncomment and adjust based on your actual models

@login_required
def index(request):
    return render(request, 'hoja_calculo/index.html', {
        'title': 'Hoja de Cálculo',
    })

@login_required
def nueva_hoja(request):
    # Logic to create a new spreadsheet
    return render(request, 'hoja_calculo/nueva_hoja.html', {
        'title': 'Nueva Hoja de Cálculo',
    })

@login_required
def mis_hojas(request):
    # hojas = HojaCalculo.objects.filter(usuario=request.user).order_by('-fecha_modificacion')
    hojas = []  # Placeholder, replace with actual query
    return render(request, 'hoja_calculo/mis_hojas.html', {
        'title': 'Mis Hojas de Cálculo',
        'hojas': hojas,
    })

@login_required
def editar_hoja(request, pk):
    # hoja = get_object_or_404(HojaCalculo, pk=pk, usuario=request.user)
    # celdas = Celda.objects.filter(hoja=hoja).order_by('fila', 'columna')
    
    return render(request, 'hoja_calculo/editar_hoja.html', {
        'title': 'Editar Hoja de Cálculo',
        # 'hoja': hoja,
        # 'celdas': celdas,
    })

@login_required
def eliminar_hoja(request, pk):
    # hoja = get_object_or_404(HojaCalculo, pk=pk, usuario=request.user)
    # Logic to delete the spreadsheet
    
    return redirect('hoja_calculo:mis_hojas')

@login_required
def importar(request):
    # Logic to import spreadsheets
    return render(request, 'hoja_calculo/importar.html', {
        'title': 'Importar Hoja de Cálculo',
    })

@login_required
def exportar(request):
    # Logic to export spreadsheets
    return render(request, 'hoja_calculo/exportar.html', {
        'title': 'Exportar Hoja de Cálculo',
    })
