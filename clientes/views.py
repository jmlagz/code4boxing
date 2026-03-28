from django.shortcuts import render, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import datetime
from .models import Cliente
from .forms import ClienteForm

#Vistas para gestión de clientes
from django.core.paginator import Paginator
from django.db.models import Q

def lista_clientes(request):
    query = request.GET.get('q')

    if query:
        lista = Cliente.objects.filter(
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        lista = Cliente.objects.all()

    paginator = Paginator(lista, 10)  # 👈 10 por página
    page_number = request.GET.get('page')
    clientes = paginator.get_page(page_number)

    return render(request, 'clientes/lista_clientes.html', {
        'clientes': clientes,
        'query': query
    })


# ✅ CREAR CLIENTE
def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/crear_cliente.html', {'form': form})

# ✅ DETALLE DE CLIENTE
def detalle_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    return render(request, 'clientes/detalle_cliente.html', {'cliente': cliente})

# ✅ EDITAR CLIENTE
def editar_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)

    if request.method == 'POST':
        form = ClienteForm(request.POST, request.FILES, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/crear_cliente.html', {'form': form})

# ✅ ELIMINAR CLIENTE
def baja_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    cliente.activo = False
    cliente.save()
    return redirect('lista_clientes')

# ✅ GENERAR PDF PROFESIONAL
def generar_contrato(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)

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

# Return the generated PDF response
import csv

def exportar_clientes_csv(request):
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

    clientes = Cliente.objects.all()

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