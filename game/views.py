from rest_framework import viewsets

from game.models import Player, Team, Match, TeamMatch
from game.serializers import PlayerSerializer, TeamSerializer, MatchSerializer, TeamMatchSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class TeamMatchViewSet(viewsets.ModelViewSet):
    queryset = TeamMatch.objects.all()
    serializer_class = TeamMatchSerializer
