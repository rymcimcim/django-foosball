# -*- coding: utf-8 -*-
import json
import requests

from game.utils import get_or_create_team
from players.models import Player
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

from game.models import Team, Match, MatchSet
from game.serializers import TeamSerializer, MatchSerializer


class APIRoot(APIView):
    def get(self, request):
        return Response({
            'players': reverse('players:player-list', request=request),
            'teams': reverse('game:team-list', request=request),
            'matches': reverse('game:match-list', request=request)
        })


class TeamList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class MatchList(generics.ListAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class MatchDetail(generics.RetrieveDestroyAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer


class SlackTestView(APIView):
    def get_data(self):
        text_list = self.request.data['text'].split(' ')

        if len(text_list) < 6:
            raise ValidationError('6 parametrów jest wymaganych')

        players = []
        for player in text_list[:4]:
            if player == 'ja':
                players.append(self.request.data['user_name'])
            else:
                players.append(player)

        scores = text_list[5:]
        ball = text_list[4]

        try:
            player1 = Player.objects.get(login=players[0])
            player2 = Player.objects.get(login=players[1])
            player3 = Player.objects.get(login=players[2])
            player4 = Player.objects.get(login=players[3])
        except Player.DoesNotExist:
            raise ValidationError('Jeden lub wieku graczy nie istnieje.')

        user_added = Player.objects.get(login=self.request.data['user_name'])
        return player1, player2, player3, player4, scores, ball, user_added

    def post(self, request, format=None):
        if 'token' not in request.data or request.data['token'] != settings.SLACK_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        player1, player2, player3, player4, scores, ball, user_added = self.get_data()

        team1 = get_or_create_team(player1, player2)
        team2 = get_or_create_team(player3, player4)


        match = Match.objects.create(
            added_by=user_added,
            team_1=team1,
            team_2=team2,
            ball=ball
        )
        for score in scores:
            points = score.split(':')
            match.add_match_set(int(points[0]), int(points[1]))
        match.calculate_score()

        return Response(match.report_score_to_slack(), status=status.HTTP_200_OK)
