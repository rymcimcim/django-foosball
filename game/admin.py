# -*- coding: utf-8 -*-

from django.contrib import admin
from game.models import Match


class MatchAdmin(admin.ModelAdmin):
    pass


admin.site.register(Match, MatchAdmin)
