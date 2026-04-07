from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.lista_clientes, name='lista_clientes'),
    path('nuevo/', views.crear_cliente, name='crear_cliente'),
    path('contrato/<int:cliente_id>/', views.generar_contrato, name='generar_contrato'),
    path('cliente/<int:cliente_id>/', views.detalle_cliente, name='detalle_cliente'),
    path('editar/<int:cliente_id>/', views.editar_cliente, name='editar_cliente'),
    path('baja/<int:cliente_id>/', views.baja_cliente, name='baja_cliente'),
    path('exportar/', views.exportar_clientes_csv, name='exportar_clientes'),
    path('clientes/', views.lista_clientes, name='lista_clientes'),

    # 🔐 Auth
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),

    # 🔁 Password reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='clientes/password_reset.html'
         ),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='clientes/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='clientes/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='clientes/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
