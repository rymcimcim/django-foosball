from django.db import models
from game.helpers import FieldHistory


class Player(FieldHistory):
    name = models.CharField(max_length=255)


class Team(FieldHistory):
    players = models.ManyToManyField(Player)


class TeamMatch(FieldHistory):
    team = models.ForeignKey(Team)
    score = models.IntegerField()
    state = models.CharField(max_length=25, choices=['win', 'lost', 'tie'])


class Match(FieldHistory):
    added_by = models.ForeignKey(Player)
    teams = models.ManyToManyField(Team)