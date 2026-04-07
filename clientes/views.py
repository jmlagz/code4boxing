from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from .forms import ClienteForm
from .models import Cliente, Gym

#Para el login
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

#para el logout
from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')

#Login requerido para acceder a todas las paginas
from django.contrib.auth.decorators import login_required

#Vista de login
from django.utils.http import url_has_allowed_host_and_scheme

def login_view(request):
    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next')

            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts=None):
                if '/reset/' not in next_url:
                    return redirect(next_url)

            return redirect('dashboard')

        else:
            error = True

    return render(request, 'clientes/login.html', {'error': error})


#Dashboard
@login_required
def dashboard(request):
    gym = Gym.objects.get(owner=request.user)
    return render(request, 'clientes/dashboard.html')
    total_clientes = Cliente.objects.filter(gym=gym).count()
    activos = Cliente.objects.filter(gym=gym, activo=True).count()
    inactivos = Cliente.objects.filter(gym=gym, activo=False).count()

    return render(request, 'clientes/dashboard.html', {
        'total_clientes': total_clientes,
        'activos': activos,
        'inactivos': inactivos,
    })

#Vistas para gestión de clientes
from django.core.paginator import Paginator
from django.db.models import Q

#✅ LISTA DE CLIENTES CON BÚSQUEDA Y PAGINACIÓN
@login_required
def lista_clientes(request):
    query = request.GET.get('q')

    # 🔥 MULTI-TENANT (BASE)
    gym = Gym.objects.filter(owner=request.user).first()
    lista = Cliente.objects.filter(gym=gym)

    if not gym:
        return redirect('dashboard')  # o donde quieras mandar si no tiene gym


    if query:
        lista = lista.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )
    

    paginator = Paginator(lista, 10)  # 👈 10 por página
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)

    return render(request, 'clientes/lista_clientes.html', {
        'clientes': clientes,
        'query': query
    })


# ✅ CREAR CLIENTE

@login_required
def crear_cliente(request):
    if request.method == 'POST':
        print("FILES:", request.FILES)
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.save(commit=False)

            # 🔥 MULTI-TENANT
            gym = Gym.objects.get(owner=request.user)
            cliente.gym = gym

            # 🔥 AUDITORÍA
            cliente.creado_por = request.user

            cliente.save()
            if cliente.certificado_medico:
                print("ARCHIVO GUARDADO EN:", cliente.certificado_medico.path)
            else:
                print("NO SE GUARDÓ EL ARCHIVO")
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/crear_cliente.html', {'form': form})

# ✅ DETALLE DE CLIENTE
from django.shortcuts import get_object_or_404
@login_required
def detalle_cliente(request, cliente_id):
        # 🔥 MULTI-TENANT
        gym = Gym.objects.get(owner=request.user)
        cliente = get_object_or_404(Cliente, id=cliente_id, gym=gym)
        return render(request, 'clientes/detalle_cliente.html', {'cliente': cliente})

# ✅ EDITAR CLIENTE
@login_required
def editar_cliente(request, cliente_id):
    gym = Gym.objects.get(owner=request.user)
    cliente = get_object_or_404(Cliente, id=cliente_id, gym=gym)

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.actualizado_por = request.user
            cliente.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/crear_cliente.html', {'form': form})

# ✅ ELIMINAR CLIENTE
def baja_cliente(request, cliente_id):
    gym = Gym.objects.get(owner=request.user)
    cliente = get_object_or_404(Cliente, id=cliente_id, gym=gym)
    cliente.activo = False
    cliente.save()
    return redirect('lista_clientes')

# ✅ GENERAR PDF PROFESIONAL
def generar_contrato(request, cliente_id):
    gym = Gym.objects.get(owner=request.user)
    cliente = get_object_or_404(Cliente, id=cliente_id, gym=gym)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{cliente.id}.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # 🏷️ Encabezado
    p.setFont("Helvetica-Bold", 18)
    p.drawString(140, 750, "CODE 4 BOXING")

    p.setFont("Helvetica", 12)
    p.drawString(180, 730, "Contrato de Servicios")

    # 📅 Fecha
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    p.drawString(400, 700, f"Fecha: {fecha_actual}")

    # 🧾 Datos del cliente
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 670, "Datos del Cliente")

    p.setFont("Helvetica", 11)
    p.drawString(50, 650, f"Nombre: {cliente.nombre} {cliente.apellido}")
    p.drawString(50, 630, f"Género: {cliente.get_genero_display()}")
    p.drawString(50, 610, f"Teléfono: {cliente.telefono}")
    p.drawString(50, 590, f"Email: {cliente.email}")
    p.drawString(50, 570, f"Tipo de inscripción: {cliente.get_tipo_inscripcion_display()}")

    # 📄 Términos
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, 530, "Términos y Condiciones")

    p.setFont("Helvetica", 10)

    texto = p.beginText(50, 510)
    texto.setLeading(14)

    contenido = [
        "El cliente acepta participar en las actividades de entrenamiento físico y boxeo bajo su propia responsabilidad.",
        "Declara contar con las condiciones de salud necesarias para realizar actividad física.",
        "Code 4 Boxing no se hace responsable por lesiones derivadas del uso indebido de las instalaciones.",
        "El cliente se compromete a respetar las reglas del gimnasio y a mantener una conducta adecuada.",
        "Este contrato tiene validez conforme al tipo de inscripción seleccionado.",
    ]

    for linea in contenido:
        texto.textLine(linea)

    p.drawText(texto)

    # ✍️ Firmas
    p.line(50, 150, 250, 150)
    p.drawString(50, 130, "Firma del Cliente")

    p.line(300, 150, 500, 150)
    p.drawString(300, 130, "Firma Autorizada")

    # Footer
    p.setFont("Helvetica-Oblique", 8)
    p.drawString(140, 50, "Code 4 Boxing - Sistema de gestión de clientes")

    p.showPage()
    p.save()
    
    return response

#Para el dashboard
from django.contrib.auth.decorators import login_required
@login_required
def dashboard(request):
    gym = Gym.objects.get(owner=request.user)
    total_clientes = Cliente.objects.filter(gym=gym).count()
    #total_clientes = Cliente.objects.count()
    activos = Cliente.objects.filter(activo=True).count()
    inactivos = Cliente.objects.filter(activo=False).count()

    return render(request, 'clientes/dashboard.html', {
        'total_clientes': total_clientes,
        'activos': activos,
        'inactivos': inactivos,
    })

#para la ruta de los archivos subidos
from django.http import FileResponse, Http404
import os
from django.conf import settings

def servir_media(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        raise Http404("Archivo no encontrado")
    

#Rutas de los archivos
from django.urls import re_path
from clientes.views import servir_media


# Return the generated PDF response
import csv
@login_required
def exportar_clientes_csv(request):
    gym = Gym.objects.get(owner=request.user)
    clientes = Cliente.objects.filter(gym=gym)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'Nombre',
        'Apellido',
        'Fecha Nacimiento',
        'Genero',
        'Telefono',
        'Email',
        'Direccion',
        'Contacto Emergencia',
        'Tipo Inscripcion',
        'Activo',
        'Fecha Inscripcion'
    ])

    
    for c in clientes:
        writer.writerow([
            c.nombre,
            c.apellido,
            c.fecha_nacimiento,
            c.get_genero_display(),
            c.telefono,
            c.email,
            c.direccion,
            c.contacto_emergencia,
            c.get_tipo_inscripcion_display(),
            'Activo' if c.activo else 'Inactivo',
            c.fecha_inscripcion
        ])

    return response