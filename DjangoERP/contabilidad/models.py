from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from core.models import Company

class CuentaContable(models.Model):
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    saldo = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Saldo")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        verbose_name = "Cuenta Contable"
        verbose_name_plural = "Cuentas Contables"
        ordering = ['codigo']

class Asiento(models.Model):
    fecha = models.DateField(verbose_name="Fecha")
    concepto = models.CharField(max_length=255, verbose_name="Concepto")
    referencia = models.CharField(max_length=50, blank=True, null=True, verbose_name="Referencia")
    # Usar referencias de cadena para evitar dependencias circulares
    compra = models.ForeignKey('compras.Compra', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Compra Relacionada")
    venta = models.ForeignKey('ventas.Venta', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Venta Relacionada")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"Asiento {self.id} - {self.concepto}"
    
    class Meta:
        verbose_name = "Asiento Contable"
        verbose_name_plural = "Asientos Contables"
        ordering = ['-fecha', '-id']

class LineaAsiento(models.Model):
    TIPO_CHOICES = [
        ('debe', 'Debe'),
        ('haber', 'Haber'),
    ]
    
    asiento = models.ForeignKey(Asiento, on_delete=models.CASCADE, related_name='lineas', verbose_name="Asiento")
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.CASCADE, verbose_name="Cuenta")
    concepto = models.CharField(max_length=255, verbose_name="Concepto")
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES, verbose_name="Tipo")
    importe = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Importe")
    
    def __str__(self):
        return f"{self.cuenta.codigo} - {self.importe} {self.tipo}"
    
    class Meta:
        verbose_name = "Línea de Asiento"
        verbose_name_plural = "Líneas de Asiento"

class AccountingAccount(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
