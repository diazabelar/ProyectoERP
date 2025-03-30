from django import forms
from .models import Cliente, Venta, LineaVenta, Factura


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion', 
                 'nif', 'codigo_postal', 'ciudad', 'provincia']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'id': 'id_email'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_telefono'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'id': 'id_direccion', 'rows': 3}),
            'nif': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_nif'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_codigo_postal'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_ciudad'}),
            'provincia': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_provincia'}),
        }



class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['numero', 'cliente', 'fecha', 'estado', 'notas']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LineaVentaForm(forms.ModelForm):
    class Meta:
        model = LineaVenta
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['numero', 'fecha_emision', 'fecha_vencimiento', 'estado']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_vencimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
