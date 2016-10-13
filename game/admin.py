# -*- coding: utf-8 -*-

from django.contrib import admin
from game.models import Match, MatchSet


class MatchSetInline(admin.TabularInline):
    model = MatchSet
    extra = 0


class MatchAdmin(admin.ModelAdmin):
    inlines = [MatchSetInline, ]
    pass


admin.site.register(Match, MatchAdmin)
