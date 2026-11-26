"""Enumerations shared across apps (user preferences and streaming links)."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Service(models.TextChoices):
    TIDAL = "tidal", _("Tidal")
    SPOTIFY = "spotify", _("Spotify")
    APPLE_MUSIC = "apple_music", _("Apple Music")
    DEEZER = "deezer", _("Deezer")
    YOUTUBE_MUSIC = "youtube_music", _("YouTube Music")
    AMAZON_MUSIC = "amazon_music", _("Amazon Music")
    BANDCAMP = "bandcamp", _("Bandcamp")
    QOBUZ = "qobuz", _("Qobuz")
    OTHER = "other", _("Outro")
