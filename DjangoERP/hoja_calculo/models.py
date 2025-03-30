from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class HojaCalculo(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    datos = models.JSONField(default=dict, verbose_name="Datos")
    privado = models.BooleanField(default=False, verbose_name="Privado")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    history = HistoricalRecords()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Hoja de Cálculo"
        verbose_name_plural = "Hojas de Cálculo"
        ordering = ['-fecha_actualizacion']
