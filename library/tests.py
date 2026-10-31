from django.test import Client, TestCase
from django.urls import reverse

from config.settings import LANGUAGE_CODE

from .models import Artista


class TestLanguageSystem(TestCase):
    def test_language_pt_br(self):
        self.assertEqual(LANGUAGE_CODE, 'pt-br')


class CadastroArtistaTests(TestCase):
    def test_cadastro_rejeita_nome_invalido_sem_alterar_registros(self):
        Artista.objects.create(nome='Iron Maiden')
        registros_antes = list(Artista.objects.values_list('pk', 'nome'))
        # Permite verificar a resposta mesmo se a view causar um erro no servidor.
        cliente = Client(raise_request_exception=False)
        url_cadastro = reverse('cadastrar_artista')

        casos = (
            ('ausente', {}),
            ('vazio', {'nome': ''}),
            ('somente espaços', {'nome': '   '}),
        )

        for caso, dados in casos:
            with self.subTest(nome=caso):
                resposta = cliente.post(url_cadastro, dados)

                self.assertContains(
                    resposta,
                    'Informe o nome do artista.',
                    status_code=400,
                )
                self.assertEqual(
                    list(Artista.objects.values_list('pk', 'nome')),
                    registros_antes,
                    'Um cadastro inválido deve preservar todos os registros.',
                )

    def test_cadastro_valido_permite_consultar_artista_sem_albuns(self):
        resposta = self.client.post(reverse('cadastrar_artista'), {'nome': 'Iron Maiden'})

        self.assertEqual(
            resposta.status_code,
            302,
            'O cadastro válido deve salvar o artista e redirecionar para sua consulta.',
        )

        # Uma nova sessão deve consultar o cadastro sem depender do POST anterior.
        consulta = Client().get(resposta['Location'])

        self.assertContains(consulta, 'Iron Maiden')
        self.assertContains(consulta, 'Nenhum álbum cadastrado')
