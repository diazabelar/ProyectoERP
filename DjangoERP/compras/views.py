from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Proveedor, Compra, LineaCompra
from django.contrib import messages
from .forms import ProveedorForm, CompraForm, LineaCompraForm

@login_required
def index(request):
    return render(request, 'compras/index.html', {
        'title': 'Gestión de Compras',
    })

@login_required
def proveedores_list(request):
    proveedores = Proveedor.objects.filter(activo=True)
    return render(request, 'compras/proveedores_list.html', {
        'title': 'Proveedores',
        'proveedores': proveedores,
    })

@login_required
def proveedor_create(request):
    # Aquí iría la lógica para crear un proveedor
    return render(request, 'compras/proveedor_form.html', {
        'title': 'Nuevo Proveedor',
    })

@login_required
def proveedor_detail(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'compras/proveedor_detail.html', {
        'title': f'Proveedor: {proveedor.nombre}',
        'proveedor': proveedor,
    })

@login_required
def proveedor_edit(request, pk):
    """
    View function for editing an existing provider.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            proveedor = form.save()
            return redirect('proveedor_detail', pk=proveedor.pk)
    else:
        form = ProveedorForm(instance=proveedor)
    
    return render(request, 'compras/proveedor_form.html', {
        'form': form,
        'proveedor': proveedor,
        'is_edit': True
    })

@login_required
def proveedor_delete(request, pk):
    """
    View function for deleting an existing provider.
    """
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        # Instead of physically deleting, set as inactive
        proveedor.activo = False
        proveedor.save()
        messages.success(request, f'Proveedor {proveedor.nombre} eliminado correctamente.')
        return redirect('compras:proveedores')
    
    return render(request, 'compras/proveedor_confirm_delete.html', {
        'title': 'Eliminar Proveedor',
        'proveedor': proveedor,
    })

@login_required
def compras_list(request):
    compras = Compra.objects.all().order_by('-fecha')
    return render(request, 'compras/compras_list.html', {
        'title': 'Pedidos de Compra',
        'compras': compras,
    })

@login_required
def compra_create(request):
    """View function for creating a new purchase order."""
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save()
            messages.success(request, f'Orden de compra {compra.numero} creada correctamente.')
            return redirect('compras:compra_detail', pk=compra.pk)
    else:
        form = CompraForm()
    
    return render(request, 'compras/compra_form.html', {
        'title': 'Nueva Orden de Compra',
        'form': form,
        'is_edit': False
    })

@login_required
def compra_detail(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    return render(request, 'compras/compra_detail.html', {
        'title': f'Compra: {compra.numero}',
        'compra': compra,
    })

@login_required
def compra_edit(request, pk):
    """
    View function for editing an existing purchase order.
    """
    compra = get_object_or_404(Compra, pk=pk)
    
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            compra = form.save()
            messages.success(request, f'Orden de compra {compra.numero} actualizada correctamente.')
            return redirect('compras:compra_detail', pk=compra.pk)
    else:
        form = CompraForm(instance=compra)
    
    return render(request, 'compras/compra_form.html', {
        'title': f'Editar Orden de Compra: {compra.numero}',
        'form': form,
        'compra': compra,
        'is_edit': True
    })

@login_required
def compra_delete(request, pk):
    """
    View function for deleting an existing purchase order.
    """
    compra = get_object_or_404(Compra, pk=pk)
    
    if request.method == 'POST':
        numero = compra.numero
        compra.delete()  # Or set an 'activo' field to False if you have one
        messages.success(request, f'Orden de compra {numero} eliminada correctamente.')
        return redirect('compras:compras')
    
    return render(request, 'compras/compra_confirm_delete.html', {
        'title': 'Eliminar Orden de Compra',
        'compra': compra,
    })

@login_required
def facturas(request):
    """Vista para gestionar facturas de proveedores"""
    return render(request, 'compras/facturas.html', {
        'titulo': 'Gestión de Facturas de Proveedores'
    })

@login_required
def factura_create(request):
    """Vista para crear una nueva factura de proveedor"""
    return render(request, 'compras/factura_form.html', {
        'titulo': 'Nueva Factura de Proveedor'
    })

def check_model_fields(request):
    from django.http import HttpResponse
    
    proveedor_fields = [f.name for f in Proveedor._meta.get_fields()]
    compra_fields = [f.name for f in Compra._meta.get_fields()]
    lineacompra_fields = [f.name for f in LineaCompra._meta.get_fields()]
    
    response = f"Proveedor fields: {proveedor_fields}<br>"
    response += f"Compra fields: {compra_fields}<br>"
    response += f"LineaCompra fields: {lineacompra_fields}<br>"
    
    return HttpResponse(response)
