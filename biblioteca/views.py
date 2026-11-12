from rest_framework.permissions import AllowAny
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class InicioView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response({}, template_name='biblioteca/inicio.html')


class CadastroView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        return Response({}, template_name='biblioteca/cadastro.html')
