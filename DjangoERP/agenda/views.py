from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Evento
from django.contrib import messages
# from .models import Cita, Tarea  # Uncomment and adjust based on your actual models

@login_required
def index(request):
    return render(request, 'agenda/index.html', {
        'title': 'Agenda',
    })

@login_required
def eventos_list(request):
    eventos = Evento.objects.filter(usuario=request.user).order_by('fecha_inicio')
    return render(request, 'agenda/eventos_list.html', {
        'title': 'Mis Eventos',
        'eventos': eventos,
    })

@login_required
def evento_create(request):
    # Aquí iría la lógica para crear un evento
    return render(request, 'agenda/evento_form.html', {
        'title': 'Nuevo Evento',
    })

@login_required
def evento_detail(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, 'agenda/evento_detail.html', {
        'title': f'Evento: {evento.titulo}',
        'evento': evento,
    })

@login_required
def citas(request):
    # citas = Cita.objects.filter(usuario=request.user).order_by('fecha', 'hora')
    citas = []  # Placeholder, replace with actual query
    return render(request, 'agenda/citas.html', {
        'title': 'Citas y Reuniones',
        'citas': citas,
    })

@login_required
def tareas(request):
    # tareas = Tarea.objects.filter(usuario=request.user, completada=False).order_by('fecha_limite')
    tareas = []  # Placeholder, replace with actual query
    return render(request, 'agenda/tareas.html', {
        'title': 'Tareas Pendientes',
        'tareas': tareas,
    })

@login_required
def calendario(request):
    # Get all events (citas and tareas) for the calendar
    return render(request, 'agenda/calendario.html', {
        'title': 'Calendario',
    })
