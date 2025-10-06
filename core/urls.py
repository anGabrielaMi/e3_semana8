from django.urls import path
from . import views

urlpatterns = [
   
   
    path('publicaciones/', views.lista_publicaciones, name='lista_publicaciones'),
    path('publicaciones/<int:publicacion_id>/', views.detalle_publicacion, name='detalle_publicacion'),
    
]