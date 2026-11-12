from django.test import SimpleTestCase


class PaginasIniciaisTests(SimpleTestCase):
    def test_inicio_mostra_link_para_cadastro(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertContains(response, '<html lang="pt-BR">')
        self.assertContains(response, '<h1>Biblioteca de álbuns</h1>', html=True)
        self.assertContains(
            response,
            '<a href="/albuns/novo/">Cadastrar álbum</a>',
            html=True,
        )

    def test_cadastro_mostra_aviso_e_link_para_voltar(self):
        response = self.client.get('/albuns/novo/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')
        self.assertContains(response, '<html lang="pt-BR">')
        self.assertContains(response, '<h1>Cadastrar álbum</h1>', html=True)
        self.assertContains(response, 'Cadastro em preparação')
        self.assertContains(
            response,
            '<a href="/">Voltar para a biblioteca</a>',
            html=True,
        )
