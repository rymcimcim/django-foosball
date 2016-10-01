# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from game.models import Player, Team, Match, TeamMatch


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        exclude = ['password']
        extra_kwargs = {
            'url': {'view_name': 'players:player-detail'}
        }
