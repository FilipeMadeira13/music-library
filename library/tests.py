from django.test import TestCase

from config.settings import LANGUAGE_CODE

class TestLanguageSystem(TestCase):
    def test_language_pt_br(self):
        self.assertEqual(LANGUAGE_CODE, 'pt-br')