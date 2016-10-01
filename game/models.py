# -*- coding: utf-8 -*-

from django.db import models
from game.helpers import FieldHistory

from players.models import Player


class Team(FieldHistory):
    players = models.ManyToManyField(Player)

    def __str__(self):
        display = ', '.join(player.login for player in self.players.all())
        return display


STATES = (
    ('win', 'win'),
    ('lost', 'lost'),
    ('tie', 'tie'),
)


class TeamMatch(FieldHistory):
    team = models.ForeignKey(Team)
    score = models.IntegerField()
    state = models.CharField(max_length=25, choices=STATES)


class Match(FieldHistory):
    added_by = models.ForeignKey(Player)
    teams = models.ManyToManyField(Team)
