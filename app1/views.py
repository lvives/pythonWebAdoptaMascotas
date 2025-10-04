from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from .models import Mascota, Persona, Adopcion, TipoMascota
from datetime import datetime
from django.urls import reverse

# Create your views here.
def home(request):
    # PREGUNTA 1 - COMPLETAR LA CARGA DE LA INFORMACION DE LA BASE DE DATOS
    tipos = TipoMascota.objects.all()
    #mascotas = Mascota.objects.select_related("tipo").all()
    mascotas = (
        Mascota.objects
        .select_related("tipo")
        .filter(estado__iexact="Disponible")
        
    )

    # PASAR LAS VARIABLES DE CONTEXTO DENTRO DE LA FUNCION RENDER
    return render(request, 'home.html', {
        'tipos': tipos,
        'mascotas': mascotas,
        "tipo_seleccionado": None
    })


def buscar(request):
    tipos = TipoMascota.objects.all()
    resultados = []
    query = ""
    if request.method == "POST":
        query = request.POST.get("filtro")
        resultados = Mascota.objects.filter(nombre__icontains=query)
    return render(request, "busqueda.html", {
        "tipos": tipos,
        "mascotas": resultados,
        "query": query
    })

def crearMascota(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        edad = request.POST.get('edad')
        descripcion = request.POST.get('descripcion')
        idtipo = request.POST.get('tipo')
        foto = request.FILES.get('foto')
        tipo = TipoMascota.objects.get(id=idtipo)

        Mascota.objects.create(
            nombre=nombre,
            edad=edad,
            descripcion=descripcion,
            foto=foto,
            tipo=tipo,
            estado="Disponible"
        )
        return HttpResponseRedirect(reverse('app1:home'))
    tipos = TipoMascota.objects.all()
    return render(request, 'crearMascota.html', {
        'tipos': tipos
    })

def crearTipo(request):
    tipos = TipoMascota.objects.all()
    return render(request,'crearTipo.html',{
        'tipos': tipos
    })

def registrarTipo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        TipoMascota.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )
        # Redirigir al home
        return HttpResponseRedirect(reverse('app1:home'))
    # Si el método no es POST, redirigir también al home
    return HttpResponseRedirect(reverse('app1:home'))

def mascotasxtipo(request, idtipo):
    tipos = TipoMascota.objects.all()
    tipo = get_object_or_404(TipoMascota, id=idtipo) 
    #mascotas = Mascota.objects.filter(tipo=tipo)
    mascotas = (
        Mascota.objects
        .select_related("tipo")
        .filter(tipo=tipo, estado__iexact="Disponible")
        .order_by("-id")
    )
    return render(request, 'home.html', {
        'tipos': tipos,
        'mascotas': mascotas,
        'tipo_seleccionado': tipo
    })

def detalleMascota(request, idMascota):
    mascota = get_object_or_404(Mascota, id=idMascota)
    tipos = TipoMascota.objects.all()
    adopcion = None
    if mascota.estado == "Adoptado":
        try:
            adopcion = Adopcion.objects.get(mascota=mascota)
        except Adopcion.DoesNotExist:
            adopcion = None

    if request.method == "POST" and mascota.estado == "Disponible":
        # INICIO DEL CODIGO
        # OBTENER DATOS DEL ADOPTANTE
        nombre = (request.POST.get("nombre") or "").strip()
        email = (request.POST.get("email") or "").strip()
        telefono = (request.POST.get("telefono") or "").strip()

        # CREAR OBJETO DE LA CLASE Persona
        persona = Persona.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono
        )

        # CREAR EL OBJETO ADOPCION, REVISAR LOS ATRIBUTOS DE LA CLASE
        # ACTUALIZAR EL ESTADO DEL OBJETO mascota A "Adoptado"
        Adopcion.objects.create(
            mascota=mascota,
            persona=persona,
            fecha_adopcion=datetime.now().strftime("%d/%m/%Y %H:%M")
        )
        mascota.estado = "Adoptado"
        mascota.save(update_fields=["estado"])
        # FIN DEL CODIGO
        # NO MODIFICAR EL RETURN DE LA PARTE FINAL
        return HttpResponseRedirect(reverse("app1:detalleMascota", args=[mascota.id]))

    return render(request, "detalleMascota.html", {
        "mascota": mascota,
        "tipos": tipos,
        "adopcion": adopcion
    })

# NO MODIFICAR ESTA VISTA
def listaAdoptantes(request):
    tipos = TipoMascota.objects.all()
    adopciones = Adopcion.objects.select_related("mascota", "persona").all()
    return render(request, "listaAdoptantes.html", {
        "adopciones": adopciones,
        "tipos": tipos
    })

