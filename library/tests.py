from django.test import Client, TestCase
from django.urls import reverse

from config.settings import LANGUAGE_CODE


class TestLanguageSystem(TestCase):
    def test_language_pt_br(self):
        self.assertEqual(LANGUAGE_CODE, 'pt-br')


class CadastroArtistaTests(TestCase):
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
