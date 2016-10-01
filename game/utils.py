# -*- coding: utf-8 -*-

from game.models import Team


def get_or_create_team(player1, player2):
    team = Team.objects.filter(players__in=[player1, player2])
    if not team:
        team = Team.objects.create()
        team.players.add(player1)
        team.players.add(player2)
        team.save()
    return team
