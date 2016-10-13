# -*- coding: utf-8 -*-
import json
import requests

from django.db import models
from django.conf import settings
from django.db.models import F
from django.db.models import Sum

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

MATCH_STATES = (
    ('win', 'win'),
    ('lost', 'lost'),
    ('tie', 'tie')
)


class Match(FieldHistory):
    added_by = models.ForeignKey(Player)
    team_1 = models.ForeignKey(Team, related_name='won_match')
    team_2 = models.ForeignKey(Team, related_name='lost_match')
    team_1_score = models.PositiveSmallIntegerField(default=0)
    team_2_score = models.PositiveSmallIntegerField(default=0)
    ball = models.CharField(choices=BALLS, default='wolna', max_length=10)
    state = models.CharField(choices=MATCH_STATES, max_length=4, blank=True, null=True)

    def __str__(self):
        return '%s vs %s:%s %s:%s' % (self.team_1, self.team_2, self.team_1_score, self.team_2_score, self.team_1_score, self.team_2_score)

    def add_match_set(self, team_1_points, team_2_points):
        MatchSet.objects.create(match=self, team_1_points=team_1_points, team_2_points=team_2_points)

    def get_team_1_total_points(self):
        return self.matchset_set.aggregate(points=Sum(F('team_1_points')))['points']

    def get_team_2_total_points(self):
        return self.matchset_set.aggregate(points=Sum(F('team_2_points')))['points']

    def get_set_scores(self):
        set_scores = self.matchset_set.values_list('team_1_points', 'team_2_points')
        resp_array = []

        for set_score in set_scores:
            resp_array.append('%s:%s' % (set_score[0], set_score[1]))

        return ' '.join(resp_array)

    def calculate_score(self):
        self.team_1_score = 0
        self.team_2_score = 0
        for match_set in self.matchset_set.all():
            if match_set.team_1_points > match_set.team_2_points:
                self.team_1_score += 1
            elif match_set.team_2_points > match_set.team_1_points:
                self.team_2_score += 1
            else:
                self.team_1_score += 1
                self.team_2_score += 1
        if self.team_1_score > self.team_2_score:
            self.state = 'win'
        elif self.team_2_score > self.team_1_score:
            self.state = 'lost'
        else:
            self.state = 'tie'
        self.save()

    def report_score_to_slack(self):
        response = {
            "username": "Adam Nawałka",
            "response_type": "in_channel",
            "attachments": [
                {
                    "fallback": "Adam Nawałka ma nową wiadomość",
                    "color": "#36a64f ",
                    "pretext": "Zakończyła się rozgrywka w piłkarzyki",
                    "title": "Mecz zakończył się wynikiem %s:%s (%s)" % (
                    str(self.team_1_score), str(self.team_2_score), self.get_set_scores()),
                    "fields": [
                        {
                            "title": "Drużyna 1",
                            "value": "%s\n%s" % (self.team_1.players.first().name, self.team_1.players.last().name),
                            "short": True
                        },
                        {
                            "title": "Drużyna 2",
                            "value": "%s\n%s" % (self.team_2.players.first().name, self.team_2.players.last().name),
                            "short": True
                        }
                    ],
                    "footer": "Rozgrywka odbyła się z użyciem %s piłki" % self.ball
                }
            ]
        }
        if settings.DEBUG is False:
            requests.post(settings.SLACK_MATCH_WEBHOOK_URL, data=json.dumps(response))
            return {}
        else:
            return json.dumps(response, indent=2)


class MatchSet(FieldHistory):
    match = models.ForeignKey(Match)
    team_1_points = models.PositiveSmallIntegerField()
    team_2_points = models.PositiveSmallIntegerField()