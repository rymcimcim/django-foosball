from rest_framework import serializers

from game.models import Player, Team, Match, TeamMatch


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class TeamMatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeamMatch
        fields = '__all__'
