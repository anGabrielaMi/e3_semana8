from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Publicacion, Categoria, Comentario

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'categoria', 'estrellas', 'fecha_publicacion')
    search_fields = ('titulo', 'contenido')
    list_filter = ('categoria', 'fecha_publicacion')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'publicacion', 'fecha_comentario')
    search_fields = ('contenido',)
    list_filter = ('fecha_comentario',)