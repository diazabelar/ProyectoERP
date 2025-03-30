from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")
    color = models.CharField(max_length=7, default="#FFFFFF", verbose_name="Color")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    history = HistoricalRecords()
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
        unique_together = ['nombre', 'usuario']

class Nota(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    contenido = models.TextField(verbose_name="Contenido")
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Categoría")
    favorito = models.BooleanField(default=False, verbose_name="Favorito")
    archivado = models.BooleanField(default=False, verbose_name="Archivado")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")
    history = HistoricalRecords()
    
    def __str__(self):
        return self.titulo
    
    class Meta:
        verbose_name = "Nota"
        verbose_name_plural = "Notas"
        ordering = ['-fecha_actualizacion']
