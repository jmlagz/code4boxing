from django.shortcuts import render
from .models import Cliente

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})

from .forms import ClienteForm
from django.shortcuts import redirect

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm()

    return render(request, 'clientes/crear_cliente.html', {'form': form})

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Cliente

def generar_contrato(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="contrato_{cliente.id}.pdf"'

    p = canvas.Canvas(response)

    p.drawString(100, 800, "CONTRATO DE SERVICIOS DE BOXEO")
    p.drawString(100, 750, f"Nombre: {cliente.nombre}")
    p.drawString(100, 730, f"Teléfono: {cliente.telefono}")
    p.drawString(100, 710, f"Email: {cliente.email}")

    p.drawString(100, 650, "El cliente acepta los términos del gimnasio.")

    p.drawString(100, 600, "Firma: _______________________")

    p.showPage()
    p.save()

    return response