from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HistorialCalculo
from django.http import JsonResponse
import json

@login_required
def index(request):
    return render(request, 'calculadora/index.html', {
        'title': 'Calculadora',
    })

@login_required
def calcular(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        operacion = request.POST.get('operacion', '')
        
        try:
            # Evaluamos la operación de manera segura
            # En un sistema real, usar una biblioteca para evaluación segura
            resultado = eval(operacion)
            
            # Guardamos en el historial
            HistorialCalculo.objects.create(
                usuario=request.user,
                operacion=operacion,
                resultado=resultado
            )
            
            return JsonResponse({
                'success': True, 
                'resultado': resultado
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def historial(request):
    historial = HistorialCalculo.objects.filter(usuario=request.user).order_by('-fecha')[:50]
    return render(request, 'calculadora/historial.html', {
        'title': 'Historial de Cálculos',
        'historial': historial,
    })

@login_required
def financiera(request):
    return render(request, 'calculadora/financiera.html', {
        'title': 'Calculadora Financiera',
    })

@login_required
def divisas(request):
    return render(request, 'calculadora/divisas.html', {
        'title': 'Conversor de Divisas',
    })

@login_required
def impuestos(request):
    return render(request, 'calculadora/impuestos.html', {
        'title': 'Calculadora de Impuestos',
    })
