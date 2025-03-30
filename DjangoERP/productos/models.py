from django.db import models
from simple_history.models import HistoricalRecords

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    history = HistoricalRecords()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']

class Producto(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código")
    nombre = models.CharField(max_length=200, verbose_name="Nombre")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoría")
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Compra")
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio de Venta")
    stock = models.IntegerField(default=0, verbose_name="Stock")
    stock_minimo = models.IntegerField(default=5, verbose_name="Stock Mínimo")
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    history = HistoricalRecords()
    
    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    @property
    def ganancia(self):
        return self.precio_venta - self.precio_compra
    
    @property
    def necesita_reposicion(self):
        return self.stock <= self.stock_minimo
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
