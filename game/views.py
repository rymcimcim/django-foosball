# -*- coding: utf-8 -*-
import json

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
        players = []
        for player in text_list[:4]:
            if player == 'ja':
                players.append(self.request.data['user_name'])
            else:
                players.append(player)

        scores = [score for score in text_list[4:6]]
        ball = text_list[len(text_list) - 1]

        try:
            player1 = Player.objects.get(login=players[0])
            player2 = Player.objects.get(login=players[1])
            player3 = Player.objects.get(login=players[2])
            player4 = Player.objects.get(login=players[3])
        except Player.DoesNotExist:
            raise ValidationError('Jeden lub wieku graczy nie istanieje.')

        user_added = Player.objects.get(login=self.request.data['user_name'])
        return player1, player2, player3, player4, scores, ball, user_added

    def get_response(self, winner_score, looser_score, winner, looser, response_ball):
        response = {
            "username": "Adam Nawałka",
            "attachments": [
                {
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": "#36a64f ",
                    "pretext": "Zakończyła się rozgrywka w piłkarzyki",
                    "title": "Mecz zakończył się wynikiem %s:%s" % (str(winner_score), str(looser_score)),
                    "fields": [
                        {
                            "title": "Zwyciężcy",
                            "value": "%s\n%s" % (winner.players.first().name, winner.players.last().name),
                            "short": True
                        },
                        {
                            "title": "Przegrani",
                            "value": "%s\n%s" % (looser.players.first().name, looser.players.last().name),
                            "short": True
                        }
                    ],
                    "footer": "Rozgrywka była z użyciem %s piłki" % response_ball
                }
            ]
        }
        return json.dumps(response)

    def get_ball(self, ball):
        if ball == 'szybka':
            response_ball = 'szybkiej'
        else:
            response_ball = 'wolnej'
        return response_ball

    def post(self, request, format=None):
        if 'token' not in request.data or request.data['token'] != settings.SLACK_TOKEN:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        player1, player2, player3, player4, scores, ball, user_added = self.get_data()

        team1 = get_or_create_team(player1, player2)
        team2 = get_or_create_team(player3, player4)

        team1_points_list = [int(score.split(':')[0]) for score in scores]
        team2_points_list = [int(score.split(':')[1]) for score in scores]
        team1_points = sum(team1_points_list)
        team2_points = sum(team2_points_list)

        team1_score = 0
        team2_score = 0
        for points1, points2 in zip(team1_points_list, team2_points_list):
            if points1 > points2:
                team1_score += 1
            else:
                team2_score += 1

        winner = team1 if team1_points > team2_points else team2

        winner_score = team1_score if team1_score > team2_score else team2_score
        winner_points = team1_points if team1_points > team2_points else team2_points
        looser = team1 if team1_points < team2_points else team2

        looser_score = team1_score if team1_score < team2_score else team2_score
        looser_points = team1_points if team1_points < team2_points else team2_points

        match = Match.objects.create(
            added_by=user_added,
            winner_team=winner,
            looser_team=looser,
            winner_score=winner_score,
            looser_score=looser_score,
            ball=ball
        )

        match_set1 = MatchSet.objects.create(
            match=match,
            winner_points=winner_points,
            looser_points=looser_points
        )

        return Response(self.get_response(winner_score, looser_score, winner, looser, self.get_ball(ball)), status=status.HTTP_200_OK, content_type='application/json')
