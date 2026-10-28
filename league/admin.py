from django.contrib import admin

from .models import Match, Player

admin.site.register(Player)
admin.site.register(Match)
