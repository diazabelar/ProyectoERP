from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from .models import Cliente
from .forms import ClienteForm
import json

from django.contrib.auth.decorators import login_required
from .models import Cliente, Venta, LineaVenta, Factura
from .forms import ClienteForm, VentaForm, LineaVentaForm, FacturaForm
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .serializers import ClienteSerializer
from rest_framework.parsers import JSONParser

@login_required
def index(request):
    # Update to use correct URL pattern names
    return render(request, 'ventas/index.html', {
        'title': 'Gestión de Ventas',
    })

# Cliente views
def clientes_list(request):
    # Check if all required fields now exist in the database
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("SHOW COLUMNS FROM ventas_cliente")
        db_columns = [col[0] for col in cursor.fetchall()]
        
    # List of columns we expect to exist
    required_columns = [
        'telefono_secundario', 'ciudad', 'provincia', 'pais', 
        'tipo_cliente', 'sitio_web', 'activo'
    ]
    
    # Check if all required columns now exist
    all_columns_exist = all(col in db_columns for col in required_columns)
    
    # If all needed columns exist, use the model directly, otherwise use raw SQL
    if all_columns_exist:
        # Removed defer('fecha_alta') from query
        clientes = Cliente.objects.all()
        if 'activo' in db_columns:
            clientes = clientes.filter(activo=True)
    else:
        # Use the raw query approach for backwards compatibility
        columns = "id, nombre, apellido, email, telefono"
        for col in ['nif', 'codigo_postal', 'direccion', 'ciudad']:
            if col in db_columns:
                columns += f", {col}"
        
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT {columns} FROM ventas_cliente")
            columns_list = [col[0] for col in cursor.description]
            clientes = [dict(zip(columns_list, row)) for row in cursor.fetchall()]
    
    form = ClienteForm()
    return render(request, 'ventas/clientes_list.html', {
        'clientes': clientes,
        'form': form,
        'existing_columns': db_columns  # Pass to template so we can conditionally render columns
    })

@require_http_methods(["GET", "POST"])
def cliente_detail(request, pk):
    """View for getting client details"""
    # Removed defer('fecha_alta') from get_object_or_404
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'GET':
        # Removed 'fecha_alta' to avoid DB errors:
        data = {
            'id': cliente.id,
            'nombre': cliente.nombre,
            'apellido': cliente.apellido,
            'email': cliente.email,
            'telefono': cliente.telefono,
            'telefono_secundario': getattr(cliente, 'telefono_secundario', ''),
            'direccion': cliente.direccion,
            'nif': cliente.nif,
            'codigo_postal': cliente.codigo_postal,
            'ciudad': cliente.ciudad,
            'provincia': cliente.provincia,
            'pais': getattr(cliente, 'pais', 'España'),
            'tipo_cliente': getattr(cliente, 'tipo_cliente', 'particular'),
            'sitio_web': getattr(cliente, 'sitio_web', ''),
            'notas': getattr(cliente, 'notas', ''),
        }
        return JsonResponse(data)
    
    # Handle other methods as needed
    return JsonResponse({'error': 'Método no permitido'}, status=405)

@require_http_methods(["GET"])
def cliente_edit(request, pk):
    """API endpoint to get client data for editing"""
    # Removed defer('fecha_alta') from get_object_or_404
    cliente = get_object_or_404(Cliente, pk=pk)
    serializer = ClienteSerializer(cliente)
    data = serializer.data
    # Remove 'fecha_alta' if present to avoid triggering refresh from DB
    data.pop('fecha_alta', None)
    return JsonResponse(data)

@require_http_methods(["POST"])
def cliente_update(request, pk):
    """API endpoint to update client data"""
    # Removed defer('fecha_alta') from get_object_or_404
    cliente = get_object_or_404(Cliente, pk=pk)
    
    try:
        data = { key: value for key, value in request.POST.items() if key not in ['csrfmiddlewaretoken', 'cliente_id'] }
        serializer = ClienteSerializer(cliente, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        else:
            # Log errors for debug information
            print("Serializer Errors:", serializer.errors)
            return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        print("Exception updating client:", str(e))
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["POST"])
def cliente_create(request):
    """API endpoint to create a new client"""
    try:
        data = {}
        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'cliente_id':
                data[key] = value
        
        serializer = ClienteSerializer(data=data)
        if serializer.is_valid():
            cliente = serializer.save()
            return JsonResponse(serializer.data)
        else:
            return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_POST
def cliente_delete(request, pk):
    """View for deleting clients"""
    cliente = get_object_or_404(Cliente, pk=pk)
    
    # Check if 'activo' column exists and use soft delete if it does
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SHOW COLUMNS FROM ventas_cliente LIKE 'activo'")
        has_activo = cursor.fetchone() is not None
    
    if has_activo:
        # Use soft delete
        cliente.activo = False
        cliente.save()
    else:
        # Use hard delete
        cliente.delete()
        
    return JsonResponse({'success': True})

# Venta views
@login_required
def ventas_list(request):
    ventas = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/ventas_list.html', {
        'title': 'Presupuestos de Venta',
        'ventas': ventas,
    })

@login_required
def venta_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user
            venta.subtotal = 0
            venta.iva = 0
            venta.total = 0
            venta.save()
            messages.success(request, f'Presupuesto {venta.numero} creado correctamente.')
            return redirect('ventas:venta_detail', pk=venta.pk)
    else:
        form = VentaForm()
    return render(request, 'ventas/presupuesto_form.html', {
        'title': 'Nuevo Presupuesto',
        'form': form,
        'is_edit': False
    })

@login_required
def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    return render(request, 'ventas/venta_detail.html', {
        'title': f'Venta: {venta.numero}',
        'venta': venta,
    })

@login_required
def venta_edit(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            venta = form.save()
            messages.success(request, f'Venta {venta.numero} actualizada correctamente.')
            return redirect('ventas:venta_detail', pk=venta.pk)
    else:
        form = VentaForm(instance=venta)
    return render(request, 'ventas/presupuesto_form.html', {
        'title': f'Editar Presupuesto #{venta.numero}',
        'form': form,
        'venta': venta,
        'is_edit': True
    })

@login_required
def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        numero = venta.numero
        venta.delete()
        messages.success(request, f'Venta {numero} eliminada correctamente.')
        return redirect('ventas:presupuestos')
    return render(request, 'ventas/venta_confirm_delete.html', {
        'title': 'Eliminar Venta',
        'venta': venta,
    })

# Presupuesto views
@login_required
def presupuesto_list(request):
    presupuestos = Venta.objects.all().order_by('-fecha')
    return render(request, 'ventas/presupuestos_list.html', {
        'title': 'Presupuestos de Venta',
        'presupuestos': presupuestos,
    })

@login_required
def presupuesto_create(request):
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            presupuesto = form.save(commit=False)
            presupuesto.usuario = request.user
            presupuesto.subtotal = 0
            presupuesto.iva = 0
            presupuesto.total = 0
            presupuesto.save()
            messages.success(request, f'Presupuesto {presupuesto.numero} creado correctamente.')
            return redirect('ventas:presupuesto_edit', pk=presupuesto.pk)
    else:
        form = VentaForm()
    return render(request, 'ventas/presupuesto_form.html', {
        'title': 'Nuevo Presupuesto',
        'form': form,
        'is_edit': False
    })

@login_required
def presupuesto_edit(request, pk):
    presupuesto = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=presupuesto)
        if form.is_valid():
            presupuesto = form.save()
            messages.success(request, f'Presupuesto {presupuesto.numero} actualizado correctamente.')
            return redirect('ventas:presupuesto_edit', pk=presupuesto.pk)
    else:
        form = VentaForm(instance=presupuesto)
    return render(request, 'ventas/presupuesto_form.html', {
        'title': f'Editar Presupuesto #{presupuesto.numero}',
        'form': form,
        'presupuesto': presupuesto,
        'is_edit': True
    })

@login_required
def presupuesto_delete(request, pk):
    presupuesto = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        numero = presupuesto.numero
        presupuesto.delete()
        messages.success(request, f'Presupuesto {numero} eliminado correctamente.')
        return redirect('ventas:presupuestos')
    return render(request, 'ventas/presupuesto_confirm_delete.html', {
        'title': 'Eliminar Presupuesto',
        'presupuesto': presupuesto,
    })

@login_required
def presupuesto_add_line(request, pk):
    presupuesto = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        line_id = request.POST.get('line_id')
        
        if line_id:  # Editing existing line
            linea = get_object_or_404(LineaVenta, pk=line_id, venta=presupuesto)
            form = LineaVentaForm(request.POST, instance=linea)
        else:  # Creating new line
            form = LineaVentaForm(request.POST)
        
        if form.is_valid():
            linea = form.save(commit=False)
            linea.venta = presupuesto
            linea.save()
            
            # Recalculate totals
            presupuesto.recalculate_totals()
            
            messages.success(request, 'Línea guardada correctamente.')
            return redirect('ventas:presupuesto_edit', pk=presupuesto.pk)
        else:
            messages.error(request, 'Error al guardar la línea.')
    return redirect('ventas:presupuesto_edit', pk=presupuesto.pk)

@login_required
def presupuesto_delete_line(request, pk):
    presupuesto = get_object_or_404(Venta, pk=pk)
    if request.method == 'DELETE':
        line_id = request.GET.get('line_id')
        if line_id:
            try:
                linea = LineaVenta.objects.get(pk=line_id, venta=presupuesto)
                linea.delete()
                
                # Recalculate totals
                presupuesto.recalculate_totals()
                
                return JsonResponse({'status': 'success'})
            except LineaVenta.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Línea no encontrada'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)

# Factura views
@login_required
def facturas_list(request):
    facturas = Factura.objects.all().order_by('-fecha_emision')
    return render(request, 'ventas/facturas_list.html', {
        'title': 'Facturas de Venta',
        'facturas': facturas,
    })

@login_required
def factura_create(request):
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save()
            messages.success(request, f'Factura {factura.numero} creada correctamente.')
            return redirect('ventas:facturas')
    else:
        form = FacturaForm()
    
    return render(request, 'ventas/factura_form.html', {
        'title': 'Nueva Factura',
        'form': form,
    })
