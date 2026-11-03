from rest_framework import serializers

from library.models import Artista

class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artista
        fields = ['pk', 'nome']