# -*- coding: utf-8 -*-

from django.db import models

from game.helpers import FieldHistory


class Player(FieldHistory):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Team(FieldHistory):
    players = models.ManyToManyField(Player)

    def __str__(self):
        display = ''
        [display.join(player.name + ', ') if index == 0 else display.join(player.name) for index, player in
         enumerate(self.players.all())]
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
