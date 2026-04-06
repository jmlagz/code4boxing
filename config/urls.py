from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from clientes import views 
from django.shortcuts import redirect

def login_redirect(request):
    return redirect('/clientes/login/')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='home'),
    path('login/', login_redirect),
    path('clientes/', include('clientes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)