from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from clientes import views
from clientes.views import servir_media
from django.shortcuts import redirect

def login_redirect(request):
    return redirect('/clientes/login/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='home'),
    path('login/', login_redirect),
    path('clientes/', include('clientes.urls')),
]

# 👇 Esto lo dejas (no estorba)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 👇 ESTA es la clave para Render
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', servir_media),
]