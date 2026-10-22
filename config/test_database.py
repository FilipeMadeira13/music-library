from django import db
from django.test import TestCase


class TestDatabase(TestCase):
    def test_database(self):
        with db.connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            database_name = cursor.fetchone()[0]
            self.assertEqual(database_name, "test_music_library_dev")
