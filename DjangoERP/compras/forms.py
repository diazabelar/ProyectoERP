from django import forms
from .models import Proveedor, Compra, LineaCompra

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        # Remove fields that don't exist in the model
        fields = '__all__'  # Use all fields, or list only the ones that exist
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # Only include other fields if they exist in your model
        }

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['numero', 'fecha', 'proveedor', 'estado', 'notas']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class LineaCompraForm(forms.ModelForm):
    class Meta:
        model = LineaCompra
        fields = ['producto', 'cantidad', 'precio_unitario']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        }
