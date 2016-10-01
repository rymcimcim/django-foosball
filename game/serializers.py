# -*- coding: utf-8 -*-

from players.serializers import PlayerSerializer
from rest_framework import serializers

from game.models import Team, Match


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = '__all__'


class MatchSerializer(serializers.ModelSerializer):
    winner_team = TeamSerializer(read_only=True)
    looser_team = TeamSerializer(read_only=True)

    class Meta:
        model = Match
        fields = '__all__'
