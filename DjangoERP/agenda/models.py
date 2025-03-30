from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Evento(models.Model):
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]
    
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_inicio = models.DateTimeField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateTimeField(verbose_name="Fecha de Fin")
    todo_el_dia = models.BooleanField(default=False, verbose_name="Todo el Día")
    ubicacion = models.CharField(max_length=200, blank=True, null=True, verbose_name="Ubicación")
    prioridad = models.CharField(max_length=5, choices=PRIORIDAD_CHOICES, default='media', verbose_name="Prioridad")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    participantes = models.ManyToManyField(User, related_name='eventos_invitado', blank=True, verbose_name="Participantes")
    completado = models.BooleanField(default=False, verbose_name="Completado")
    recordatorio = models.IntegerField(default=30, verbose_name="Recordatorio (minutos)")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    history = HistoricalRecords()
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['-fecha_inicio']
