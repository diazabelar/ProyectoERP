from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CuentaContable, Asiento, LineaAsiento
from django.contrib import messages
from django.urls import reverse
from .forms import CuentaForm, AccountingAccountForm  # You might need to create this form

@login_required
def index(request):
    return render(request, 'contabilidad/index.html', {
        'title': 'Gestión de Contabilidad',
    })

@login_required
def cuentas_list(request):
    cuentas = CuentaContable.objects.all().order_by('codigo')
    return render(request, 'contabilidad/cuentas_list.html', {
        'title': 'Plan de Cuentas',
        'cuentas': cuentas,
    })

@login_required
def cuenta_create(request):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contabilidad:cuentas_list')
    else:
        form = CuentaForm()
    return render(request, 'contabilidad/cuenta_form.html', {
        'title': 'Nueva Cuenta Contable',
        'form': form,
    })

@login_required
def cuenta_detail(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    return render(request, 'contabilidad/cuenta_detail.html', {
        'title': f'Cuenta: {cuenta.codigo} - {cuenta.nombre}',
        'cuenta': cuenta,
    })

@login_required
def cuenta_update(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            return redirect('contabilidad:cuentas_list')
    else:
        form = CuentaForm(instance=cuenta)
    return render(request, 'contabilidad/cuenta_form.html', {
        'form': form,
    })

@login_required
def cuenta_delete(request, pk):
    cuenta = get_object_or_404(CuentaContable, pk=pk)
    if request.method == 'POST':
        cuenta.delete()
        messages.success(request, f'La cuenta {cuenta.codigo} - {cuenta.nombre} ha sido eliminada.')
        return redirect('contabilidad:cuentas_list')
    return render(request, 'contabilidad/cuenta_confirm_delete.html', {
        'cuenta': cuenta,
        'title': 'Eliminar Cuenta',
    })

@login_required
def asientos_list(request):
    asientos = Asiento.objects.all().order_by('-fecha', '-id')
    return render(request, 'contabilidad/asientos_list.html', {
        'title': 'Libro Diario',
        'asientos': asientos,
    })

@login_required
def asiento_create(request):
    # Aquí iría la lógica para crear un asiento contable
    return render(request, 'contabilidad/asiento_form.html', {
        'title': 'Nuevo Asiento Contable',
    })

@login_required
def asiento_detail(request, pk):
    asiento = get_object_or_404(Asiento, pk=pk)
    return render(request, 'contabilidad/asiento_detail.html', {
        'title': f'Asiento: {asiento.id}',
        'asiento': asiento,
    })

def create_account_view(request):
    if request.method == 'POST':
        form = AccountingAccountForm(request.POST, company=request.company)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.company = request.company
            instance.save()
            return redirect('account_list')  # Replace with your actual URL
    else:
        form = AccountingAccountForm(company=request.company)
    return render(request, 'contabilidad/account_form.html', {'form': form})
