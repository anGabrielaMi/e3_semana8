# ─── IMPORTACIONES ─────────────────────────────────────────────────────────────
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate, login


from core.models import Publicacion, Categoria

# ─── VISTAS GENERALES ──────────────────────────────────────────────────────────
def inicio(request):
    return render(request, 'index.html', {
        'usuario_autenticado': request.user.is_authenticated,
        'usuario_nombre': request.user.username if request.user.is_authenticated else ''
    })

def contrasena(request):
    return render(request, 'recuperarContrasena.html')

def perfil(request):
    return render(request, 'modificarPerfil.html')

# ─── AUTENTICACIÓN FORMULARIO ──────────────────────────────────────────────────
def ingresar(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        print(f"[DEBUG] Intento de login → email: '{email}', password: '{password}'")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Credenciales inválidas.")
    return render(request, 'inicioSesion.html')

def registrar(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('tipo_usuario')
        codigo = request.POST.get('codigo_admin')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
        elif rol == "administrador" and codigo != "FICCIONA2025":
            messages.error(request, "Código de administrador inválido.")
        else:
            nuevo_usuario = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombre
            )
            if rol == "administrador" and codigo == "FICCIONA2025":
                nuevo_usuario.is_staff = True
                nuevo_usuario.is_superuser = True

            nuevo_usuario.save()
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('ingresar')

    return render(request, 'registro.html')

# ─── AUTENTICACIÓN AJAX ────────────────────────────────────────────────────────



@csrf_exempt  # ← Esto permite que funcione sin token CSRF por ahora
def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)

            # Esto fuerza la creación del token CSRF y asegura que la sesión se active
            get_token(request)

            redirect_url = '/admin-panel/' if user.is_staff else '/'
            return JsonResponse({'redirect_url': redirect_url})
        else:
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

# ─── PANEL DE ADMINISTRACIÓN ───────────────────────────────────────────────────
def es_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(es_admin)
def panel_admin(request):
    usuarios = User.objects.all()
    return render(request, 'admin_panel.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
        else:
            nuevo_usuario = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombre
            )
            if rol == "admin":
                nuevo_usuario.is_staff = True
            nuevo_usuario.save()
            messages.success(request, "Usuario creado correctamente.")

        return redirect('admin_panel')

@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    usuario.delete()
    messages.success(request, "Usuario eliminado.")
    return redirect('admin_panel')

@login_required
@user_passes_test(es_admin)
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        usuario.first_name = request.POST.get('nombre')
        usuario.email = request.POST.get('email')
        usuario.username = request.POST.get('email')  # mantener coherencia
        usuario.is_staff = request.POST.get('rol') == "admin"
        usuario.save()
        messages.success(request, "Usuario actualizado.")
        return redirect('admin_panel')
    return render(request, 'editar_usuario.html', {'usuario': usuario})

# ─── SECCIONES TEMÁTICAS ───────────────────────────────────────────────────────
def resenas_por_categoria(request, categoria):
    plantilla = f"{categoria}.html"

    try:
        categoria_obj = Categoria.objects.get(nombre__iexact=categoria)
        publicaciones = Publicacion.objects.filter(categoria=categoria_obj).order_by('-fecha_publicacion')
    except Categoria.DoesNotExist:
        publicaciones = []

    return render(request, plantilla, {
        'categoria': categoria,
        'publicaciones': publicaciones,
        'usuario_autenticado': request.user.is_authenticated,
        'usuario_nombre': request.user.username if request.user.is_authenticated else ''
    })

# ─── RESEÑAS ───────────────────────────────────────────────────────────────────
@csrf_exempt
@login_required
def publicar_reseña(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            titulo = data.get('titulo')
            contenido = data.get('comentario')
            categoria_id = data.get('categoria')
            estrellas = int(data.get('estrellas', 0))

            if not titulo or not contenido or not categoria_id or estrellas not in range(1, 6):
                return JsonResponse({'error': 'Datos incompletos o inválidos'}, status=400)

            try:
                categoria_obj = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                return JsonResponse({'error': 'Categoría inválida'}, status=400)

            Publicacion.objects.create(
                usuario=request.user,
                titulo=titulo,
                contenido=contenido,
                categoria=categoria_obj,
                estrellas=estrellas
            )
            return JsonResponse({'mensaje': 'Reseña publicada correctamente'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato JSON inválido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

# ─── CERRAR SESIÓN ─────────────────────────────────────────────────────────────
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')

# ─── API PÚBLICA: LIBROS POR CATEGORÍA ─────────────────────────────────────────
def libros_por_categoria(request, categoria):
    url = f'https://openlibrary.org/subjects/{categoria}.json?limit=5'
    response = requests.get(url)
    data = response.json()
    libros = data.get('works', [])
    return render(request, 'libros_categoria.html', {
        'libros': libros,
        'categoria': categoria
    })
    
    
    
    
    
    #----------------------------


@login_required
def estado_usuario(request):
    return JsonResponse({'usuario': request.user.username})



#-------------------------------------



def obtener_reseñas(request):
    reseñas = Publicacion.objects.all().values('titulo', 'contenido', 'estrellas', 'usuario__username')
    return JsonResponse(list(reseñas), safe=False)