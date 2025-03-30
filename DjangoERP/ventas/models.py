from django.db import models
from django.contrib.auth.models import User
from productos.models import Producto
from simple_history.models import HistoricalRecords
from django.utils import timezone

class Cliente(models.Model):
    TIPO_CHOICES = [
        ('particular', 'Particular'),
        ('empresa', 'Empresa'),
        ('autonomo', 'Autónomo'),
    ]
    
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=254)
    telefono = models.CharField(max_length=20)
    telefono_secundario = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    nif = models.CharField(max_length=20, blank=True, null=True)
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    ciudad = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    pais = models.CharField(max_length=100, default='España', blank=True, null=True)
    tipo_cliente = models.CharField(max_length=20, choices=TIPO_CHOICES, default='particular')
    sitio_web = models.URLField(blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)  # Added for soft delete functionality
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Venta(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviada', 'Enviada'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]
    
    numero = models.CharField(max_length=20, unique=True, verbose_name="Número")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
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
        return f"Venta {self.numero} - {self.cliente}"
    
    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-fecha']

class LineaVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='lineas', verbose_name="Venta")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    cantidad = models.IntegerField(verbose_name="Cantidad")
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")
    
    def __str__(self):
        return f"{self.producto.nombre} ({self.cantidad})"
    
    class Meta:
        verbose_name = "Línea de Venta"
        verbose_name_plural = "Líneas de Venta"

class Presupuesto(models.Model):
    """Modelo para representar un presupuesto."""
    ESTADO_CHOICES = [
        ('BOR', 'Borrador'),
        ('ENV', 'Enviado'),
        ('ACE', 'Aceptado'),
        ('REC', 'Rechazado'),
    ]
    
    numero = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_emision = models.DateField(default=timezone.now)
    fecha_validez = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='BOR')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True)

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"

    def __str__(self):
        return self.numero

    def calcular_totales(self):
        """Calcula y actualiza los totales del presupuesto."""
        subtotal = sum(linea.subtotal_linea for linea in self.lineas.all())
        impuestos = 0  # Assuming no impuestos for now
        total = subtotal + impuestos

        self.subtotal = subtotal
        self.impuestos = impuestos
        self.total = total

class LineaPresupuesto(models.Model):
    """Modelo para representar una línea individual dentro de un presupuesto."""
    presupuesto = models.ForeignKey(Presupuesto, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_linea = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Línea de Presupuesto"
        verbose_name_plural = "Líneas de Presupuesto"

    def __str__(self):
        return f"Línea para {self.presupuesto.numero}"

    def save(self, *args, **kwargs):
        """Override del método save para calcular el subtotal de la línea."""
        self.subtotal_linea = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

class Factura(models.Model):
    """Modelo para representar una factura."""
    ESTADO_CHOICES = [
        ('BOR', 'Borrador'),
        ('ENV', 'Enviado'),
        ('PAG', 'Pagada'),
        ('ANU', 'Anulada'),
    ]

    numero = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha_emision = models.DateField(default=timezone.now)
    fecha_vencimiento = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=3, choices=ESTADO_CHOICES, default='BOR')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notas = models.TextField(blank=True)
    presupuesto_origen = models.OneToOneField(
        Presupuesto, on_delete=models.SET_NULL, null=True, blank=True, related_name='factura_generada'
    )

    class Meta:
        verbose_name = "Factura"
        verbose_name_plural = "Facturas"

    def __str__(self):
        return self.numero

    @property
    def saldo_pendiente(self):
        """Calcula el saldo pendiente de la factura."""
        return self.total - self.total_pagado

    def calcular_totales(self):
        """Calcula y actualiza los totales de la factura."""
        subtotal = sum(linea.subtotal_linea for linea in self.lineas.all())
        impuestos = 0  # Assuming no impuestos for now
        total = subtotal + impuestos

        self.subtotal = subtotal
        self.impuestos = impuestos
        self.total = total

class LineaFactura(models.Model):
    """Modelo para representar una línea individual dentro de una factura."""
    factura = models.ForeignKey(Factura, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, null=True, blank=True)
    descripcion = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_linea = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Línea de Factura"
        verbose_name_plural = "Líneas de Factura"

    def __str__(self):
        return f"Línea para {self.factura.numero}"

    def save(self, *args, **kwargs):
        """Override del método save para calcular el subtotal de la línea."""
        self.subtotal_linea = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
