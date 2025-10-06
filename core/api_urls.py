from django.urls import path
from . import views

urlpatterns = [
    path('publicaciones/', views.api_publicaciones, name='api_publicaciones'),
    path('publicaciones/crear/', views.crear_publicacion, name='crear_publicacion'),
    path('publicaciones/eliminar/<int:id>/', views.eliminar_publicacion, name='eliminar_publicacion'),
]