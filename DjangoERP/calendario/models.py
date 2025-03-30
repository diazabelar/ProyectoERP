from django.db import models
from simple_history.models import HistoricalRecords

class DiaFestivo(models.Model):
    TIPO_CHOICES = [
        ('nacional', 'Nacional'),
        ('autonomico', 'Autonómico'),
        ('local', 'Local'),
        ('empresa', 'Empresa'),
    ]
    
    fecha = models.DateField(verbose_name="Fecha")
    descripcion = models.CharField(max_length=200, verbose_name="Descripción")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, verbose_name="Tipo")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.fecha} - {self.descripcion}"
    
    class Meta:
        verbose_name = "Día Festivo"
        verbose_name_plural = "Días Festivos"
        ordering = ['fecha']
        unique_together = ['fecha', 'tipo']

class Horario(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    hora_inicio = models.TimeField(verbose_name="Hora de Inicio")
    hora_fin = models.TimeField(verbose_name="Hora de Fin")
    descanso_inicio = models.TimeField(blank=True, null=True, verbose_name="Inicio de Descanso")
    descanso_fin = models.TimeField(blank=True, null=True, verbose_name="Fin de Descanso")
    lunes = models.BooleanField(default=True, verbose_name="Lunes")
    martes = models.BooleanField(default=True, verbose_name="Martes")
    miercoles = models.BooleanField(default=True, verbose_name="Miércoles")
    jueves = models.BooleanField(default=True, verbose_name="Jueves")
    viernes = models.BooleanField(default=True, verbose_name="Viernes")
    sabado = models.BooleanField(default=False, verbose_name="Sábado")
    domingo = models.BooleanField(default=False, verbose_name="Domingo")
    history = HistoricalRecords()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Horario"
        verbose_name_plural = "Horarios"
