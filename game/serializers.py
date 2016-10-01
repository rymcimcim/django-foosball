# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from game.models import Player, Team, Match, TeamMatch


class TeamCreateSerializer(serializers.Serializer):
    player1 = serializers.CharField(max_length=255, min_length=3)
    player2 = serializers.CharField(max_length=255, min_length=3)
    player3 = serializers.CharField(max_length=255, min_length=3, allow_null=True)
    player4 = serializers.CharField(max_length=255, min_length=3, allow_null=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def save(self, **kwargs):
        player1_name = self.validated_data['player1']
        player2_name = self.validated_data['player2']
        player3_name = self.validated_data['player3']
        player4_name = self.validated_data['player4']

        if player1_name and player2_name and player3_name and player4_name:
            if player1_name in [player2_name, player3_name, player4_name] or \
                            player2_name in [player1_name, player3_name, player4_name] or \
                            player3_name in [player1_name, player2_name, player4_name] or \
                            player4_name in [player1_name, player2_name, player3_name]:
                raise ValidationError('One or more players are duplicated.')

            team1 = Team.objects.filter(players__name=player1_name).filter(players__name=player2_name)
            team2 = Team.objects.filter(players__name=player3_name).filter(players__name=player4_name)
            if len(team1) == 0:

                player1, created = Player.objects.get_or_create(name=player1_name)
                player2, created = Player.objects.get_or_create(name=player2_name)

                if len(team2) == 0:
                    player3, created = Player.objects.get_or_create(name=player3_name)
                    player4, created = Player.objects.get_or_create(name=player4_name)

                    team2 = Team.objects.create()
                    team2.players.add(player3)
                    team2.players.add(player4)
                else:
                    raise ValidationError('Team with those players exists.')

                team1 = Team.objects.create()
                team1.players.add(player1)
                team1.players.add(player2)
                return team1, team2
            raise ValidationError('Team with those players already exists.')

        elif player1_name and player2_name and (player3_name or player4_name):
            raise ValidationError('You must specify 2 or 4 players.')

        elif player1_name and player2_name:
            if player1_name != player2_name:
                team = Team.objects.filter(players__name=player1_name).filter(players__name=player2_name)
                if len(team) == 0:
                    player1, created = Player.objects.get_or_create(name=player1_name)
                    player2, created = Player.objects.get_or_create(name=player2_name)
                    team = Team.objects.create()
                    team.players.add(player1)
                    team.players.add(player2)
                    return team
                raise ValidationError('Team already exists.')
            if player1_name == player2_name:
                raise ValidationError('Players must be different.')
        else:
            raise ValidationError('You must specify at least 2 players.')


class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        extra_kwargs = {
            'url': {'view_name': 'game:team-retrive-destroy'},
            'players': {'view_name': 'game:player-detail'}
        }


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class TeamMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMatch
        fields = '__all__'
