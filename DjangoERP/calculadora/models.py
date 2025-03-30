from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class HistorialCalculo(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    operacion = models.CharField(max_length=255, verbose_name="Operación")
    resultado = models.DecimalField(max_digits=15, decimal_places=5, verbose_name="Resultado")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.operacion} = {self.resultado}"
    
    class Meta:
        verbose_name = "Historial de Cálculo"
        verbose_name_plural = "Historial de Cálculos"
        ordering = ['-fecha']
