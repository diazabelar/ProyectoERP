from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto
from simple_history.models import HistoricalRecords

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    rif = models.CharField(max_length=20, blank=True, null=True)  
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    nif = models.CharField(max_length=20, unique=True, verbose_name="NIF/CIF")
    persona_contacto = models.CharField(max_length=200, blank=True, null=True, verbose_name="Persona de Contacto")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal")
    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")
    provincia = models.CharField(max_length=100, verbose_name="Provincia")
    history = HistoricalRecords()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']

class Compra(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Proveedor")
    fecha = models.DateField(verbose_name="Fecha")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente', verbose_name="Estado")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    iva = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="IVA")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total")
    notas = models.TextField(blank=True, null=True, verbose_name="Notas")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"Compra {self.numero} - {self.proveedor}"
    
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"
        ordering = ['-fecha']

class LineaCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='lineas', verbose_name="Compra")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    
    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad})"
    
    class Meta:
        verbose_name = "Línea de Compra"
        verbose_name_plural = "Líneas de Compra"
