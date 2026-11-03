from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import permissions, viewsets

from library.serializers import ArtistaSerializer

from .models import Artista


class ArtistaViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all().order_by('nome')
    serializer_class = ArtistaSerializer
    permission_classes = [permissions.IsAuthenticated]


@require_POST
def cadastrar_artista(request):
    nome = request.POST.get('nome', '')
    if not nome.strip():
        return HttpResponseBadRequest('Informe o nome do artista.')

    artista = Artista.objects.create(nome=nome)
    return redirect('consultar_artista', pk=artista.pk)


def consultar_artista(request, pk):
    artista = get_object_or_404(Artista, pk=pk)
    return render(request, 'library/artista.html', {'artista': artista})
