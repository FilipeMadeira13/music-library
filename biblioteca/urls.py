from django.urls import path

from .views import CadastroView, InicioView

app_name = 'biblioteca'

urlpatterns = [
    path('', InicioView.as_view(), name='inicio'),
    path('albuns/novo/', CadastroView.as_view(), name='cadastro'),
]
