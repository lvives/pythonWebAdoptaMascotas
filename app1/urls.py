from django.urls import path, include
from . import views

app_name = 'app1'

urlpatterns = [
    path('',views.home, name='home'),
    path('buscar',views.buscar,name='buscar'),
    path('crearMascota', views.crearMascota,name='crearMascota'),
    path('crearTipo', views.crearTipo, name='crearTipo'),
    path('mascotasxtipo/<int:idtipo>',views.mascotasxtipo, name='mascotasxtipo'),
    path('detalleMascota/<int:idMascota>',views.detalleMascota, name='detalleMascota'),
    path('listaAdoptantes/', views.listaAdoptantes, name='listaAdoptantes'),
    path('registrarTipo',views.registrarTipo,name='registrarTipo')

]