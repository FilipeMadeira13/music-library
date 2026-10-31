from django.db import models


class Artista(models.Model):
    nome = models.CharField(max_length=255)
