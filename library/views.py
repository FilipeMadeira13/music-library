from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Artista


@require_POST
def cadastrar_artista(request):
    artista = Artista.objects.create(nome=request.POST['nome'])
    return redirect('consultar_artista', pk=artista.pk)


def consultar_artista(request, pk):
    artista = get_object_or_404(Artista, pk=pk)
    return render(request, 'library/artista.html', {'artista': artista})
