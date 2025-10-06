from rest_framework import serializers
from core.models import Publicacion

class PublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publicacion
        fields = '__all__'
        extra_kwargs = {
            'usuario': {'required': False}
        }