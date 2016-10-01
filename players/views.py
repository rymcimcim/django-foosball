# -*- coding: utf-8 -*-

from rest_framework import generics

from players.models import Player
from players.serializers import PlayerSerializer


class PlayersList(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class PlayersDetail(generics.RetrieveAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
