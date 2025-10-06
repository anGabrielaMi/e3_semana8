from django.shortcuts import render, get_object_or_404
from core.models import Publicacion
from django.views.decorators.csrf import csrf_exempt

# Vista para listar publicaciones
def lista_publicaciones(request):
    publicaciones = Publicacion.objects.select_related('usuario').all()
    return render(request, 'core/lista_publicaciones.html', {'publicaciones': publicaciones})

# Vista para ver detalle de una publicación
def detalle_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(Publicacion, pk=publicacion_id)
    return render(request, 'core/detalle_publicacion.html', {'publicacion': publicacion})



#vista tipo API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Publicacion
from .serializers import PublicacionSerializer

@api_view(['GET'])
def api_publicaciones(request):
    publicaciones = Publicacion.objects.all()
    serializer = PublicacionSerializer(publicaciones, many=True)
    return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.serializers import PublicacionSerializer
from core.models import Publicacion


@csrf_exempt
@api_view(['POST'])
def crear_publicacion(request):
    serializer = PublicacionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(usuario=request.user)  # asociar al usuario
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['DELETE'])
def eliminar_publicacion(request, id):
    publicacion = get_object_or_404(Publicacion, pk=id)
    publicacion.delete()
    return Response({'mensaje': 'Publicación eliminada'}, status=status.HTTP_204_NO_CONTENT)