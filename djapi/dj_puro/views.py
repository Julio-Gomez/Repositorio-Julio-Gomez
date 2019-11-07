from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

from .models import Categoria
# Create your views here.
def categoria_list(request):
    MAX_OBJECT = 20
    cat = Categoria.objects.all()[:MAX_OBJECT]
    data = {'results': list(cat.values('descripcion','activo'))}
    return JsonResponse(data)

def categoria_detalle(request, pk):
    cat = get_object_or_404(Categoria, pk=pk)
    data = {
        'results':{
            'descripcion': cat.descripcion,
            'activo': cat.activo
        }
    }
    return JsonResponse(data)