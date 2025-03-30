from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DiaFestivo, Horario
from django.contrib import messages

@login_required
def index(request):
    return render(request, 'calendario/index.html', {
        'title': 'Calendario',
    })

@login_required
def festivos_list(request):
    festivos = DiaFestivo.objects.all().order_by('fecha')
    return render(request, 'calendario/festivos_list.html', {
        'title': 'Días Festivos',
        'festivos': festivos,
    })

@login_required
def festivo_create(request):
    # Aquí iría la lógica para crear un día festivo
    return render(request, 'calendario/festivo_form.html', {
        'title': 'Nuevo Día Festivo',
    })

@login_required
def horarios_list(request):
    horarios = Horario.objects.all()
    return render(request, 'calendario/horarios_list.html', {
        'title': 'Horarios',
        'horarios': horarios,
    })

@login_required
def horario_create(request):
    # Aquí iría la lógica para crear un horario
    return render(request, 'calendario/horario_form.html', {
        'title': 'Nuevo Horario',
    })

@login_required
def vista_mensual(request):
    # Logic to get events for monthly view
    return render(request, 'calendario/vista_mensual.html', {
        'title': 'Vista Mensual',
    })

@login_required
def eventos(request):
    # eventos = Evento.objects.filter(usuario=request.user).order_by('fecha')
    eventos = []  # Placeholder, replace with actual query
    return render(request, 'calendario/eventos.html', {
        'title': 'Mis Eventos',
        'eventos': eventos,
    })

@login_required
def sincronizacion(request):
    return render(request, 'calendario/sincronizacion.html', {
        'title': 'Sincronización de Calendario',
    })
