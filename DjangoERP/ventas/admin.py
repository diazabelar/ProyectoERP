from django.contrib import admin
from .models import Cliente, Venta, LineaVenta, Factura, Presupuesto, LineaPresupuesto, LineaFactura

# Register your models here.
admin.site.register(Cliente)
admin.site.register(Venta)
admin.site.register(LineaVenta)

class LineaPresupuestoInline(admin.TabularInline):
    model = LineaPresupuesto
    extra = 1

class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'fecha_emision', 'estado', 'total')
    list_filter = ('estado', 'fecha_emision', 'cliente')
    search_fields = ('numero', 'cliente__nombre')
    inlines = [LineaPresupuestoInline]

admin.site.register(Presupuesto, PresupuestoAdmin)

class LineaFacturaInline(admin.TabularInline):
    model = LineaFactura
    extra = 1

class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'cliente', 'fecha_emision', 'estado', 'total', 'saldo_pendiente')
    list_filter = ('estado', 'fecha_emision', 'cliente')
    search_fields = ('numero', 'cliente__nombre')
    inlines = [LineaFacturaInline]
    readonly_fields = ('total_pagado',)

admin.site.register(Factura, FacturaAdmin)
