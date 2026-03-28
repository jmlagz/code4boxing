from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('nuevo/', views.crear_cliente, name='crear_cliente'),
    path('contrato/<int:cliente_id>/', views.generar_contrato, name='generar_contrato'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('baja/<int:cliente_id>/', views.baja_cliente, name='baja_cliente'),
    path('exportar/', views.exportar_clientes_csv, name='exportar_clientes'),
]