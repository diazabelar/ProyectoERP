from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Categoria, Producto
from django.contrib import messages

@login_required
def index(request):
    return render(request, 'productos/index.html', {
        'title': 'Gestión de Productos',
    })

@login_required
def categorias_list(request):
    categorias = Categoria.objects.filter(activo=True)
    return render(request, 'productos/categorias_list.html', {
        'title': 'Categorías',
        'categorias': categorias,
    })

@login_required
def categoria_create(request):
    # Aquí iría la lógica para crear una categoría
    return render(request, 'productos/categoria_form.html', {
        'title': 'Nueva Categoría',
    })

@login_required
def categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, 'productos/categoria_detail.html', {
        'title': f'Categoría: {categoria.nombre}',
        'categoria': categoria,
    })

@login_required
def productos_list(request):
    productos = Producto.objects.filter(activo=True)
    return render(request, 'productos/productos_list.html', {
        'title': 'Productos',
        'productos': productos,
    })

@login_required
def producto_create(request):
    # Aquí iría la lógica para crear un producto
    return render(request, 'productos/producto_form.html', {
        'title': 'Nuevo Producto',
    })

@login_required
def producto_detail(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_detail.html', {
        'title': f'Producto: {producto.nombre}',
        'producto': producto,
    })

@login_required
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {
        'productos': productos,
        'title': 'Catálogo de Productos',
    })

@login_required
def crear_producto(request):
    # Implementación básica que deberás completar
    return render(request, 'productos/producto_form.html', {
        'title': 'Nuevo Producto',
    })

@login_required
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_detail.html', {
        'producto': producto,
        'title': f'Producto: {producto.nombre}',
    })

@login_required
def editar_producto(request, pk):
    # Implementación básica que deberás completar
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'productos/producto_form.html', {
        'producto': producto,
        'title': f'Editar Producto: {producto.nombre}',
    })

@login_required
def categorias(request):
    # categorias = Categoria.objects.all().order_by('nombre')  # Uncomment and adjust based on your actual models
    categorias = []  # Placeholder, replace with actual query
    return render(request, 'productos/categorias.html', {
        'title': 'Categorías de Productos',
        'categorias': categorias,
    })

@login_required
def inventario(request):
    # items = Inventario.objects.all().order_by('-fecha_actualizacion')  # Uncomment and adjust based on your actual models
    items = []  # Placeholder, replace with actual query
    return render(request, 'productos/inventario.html', {
        'title': 'Control de Inventario',
        'items': items,
    })
