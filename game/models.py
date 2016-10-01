# -*- coding: utf-8 -*-

from django.db import models

from game.helpers import FieldHistory
from players.models import Player


class Team(FieldHistory):
    players = models.ManyToManyField(Player)

    def __str__(self):
        display = ', '.join(player.login for player in self.players.all())
        return display


BALLS = (
    ('wolna', 'wolna'),
    ('szybka', 'szybka'),
)


class Match(FieldHistory):
    added_by = models.ForeignKey(Player)
    winner_team = models.ForeignKey(Team, related_name='won_match')
    looser_team = models.ForeignKey(Team, related_name='lost_match')
    winner_score = models.PositiveSmallIntegerField()
    looser_score = models.PositiveSmallIntegerField()
    ball = models.CharField(choices=BALLS, default='wolna', max_length=10)


class MatchSet(FieldHistory):
    match = models.ForeignKey(Match)
    winner_points = models.PositiveSmallIntegerField()
    looser_points = models.PositiveSmallIntegerField()



# class TeamMatch(FieldHistory):
#     team = models.ForeignKey(Team)
#     match = models.ForeignKey(Match)
#     won = models.PositiveSmallIntegerField()
#     lost = models.PositiveSmallIntegerField()
#     state = models.CharField(max_length=10, choices=STATES)
