from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    email = serializers.CharField()  # Override email to allow any text

    class Meta:
        model = Cliente
        # Use fields instead of exclude to explicitly list only valid fields
        fields = [
            'id', 'nombre', 'apellido', 'email', 'telefono', 
            'telefono_secundario', 'direccion', 'nif', 'codigo_postal',
            'ciudad', 'provincia', 'pais', 'tipo_cliente', 
            'sitio_web', 'notas', 'activo', 'fecha_creacion', 'fecha_actualizacion'
        ]
        extra_kwargs = {
            'nif': {'required': False, 'allow_blank': True},
            'telefono_secundario': {'required': False, 'allow_blank': True},
            'sitio_web': {'required': False, 'allow_blank': True},
            'notas': {'required': False, 'allow_blank': True},
            'codigo_postal': {'required': False, 'allow_blank': True},
            'ciudad': {'required': False, 'allow_blank': True},
            'provincia': {'required': False, 'allow_blank': True},
            'pais': {'required': False, 'allow_blank': True},
            'tipo_cliente': {'required': False, 'allow_blank': True},
        }
        
    def validate_email(self, value):
        # Permitir cualquier texto sin validación de formato
        return value

    def create(self, validated_data):
        # Create the client using only the validated data
        return Cliente.objects.create(**validated_data)
