from django.urls import path
from . import views
from .views import login_usuario

urlpatterns = [
    # Navegación general
    path('inicio/', views.inicio, name="inicio"),
    path('ingresar/', views.ingresar, name="ingresar"),
    path('registrar/', views.registrar, name="registrar"),
    path('contrasena/', views.contrasena, name="contrasena"),
    path('perfil/', views.perfil, name="perfil"),
    path('logout/', views.cerrar_sesion, name='logout'),
    path('', views.inicio, name="inicio"),
    path('login-ajax/', login_usuario, name='login_ajax'),


    # Secciones temáticas
   path('<str:categoria>/', views.resenas_por_categoria, name='resenas_por_categoria'),

    # Autenticación y panel
    path('login-usuario/', views.login_usuario, name='login_usuario'),
    path('admin-panel/', views.panel_admin, name='admin_panel'),
    #path('inicio-usuario/', views.inicio_usuario, name='inicio_usuario'),

    # Gestión de usuarios
    path('crear-usuario/', views.crear_usuario, name='crear_usuario'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),

    # Funcionalidad de reseñas
    path('publicar-reseña/', views.publicar_reseña, name='publicar_reseña'),
    
    #Api
    path('libros/<str:categoria>/', views.libros_por_categoria, name='libros_por_categoria')

]
