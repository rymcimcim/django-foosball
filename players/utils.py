# -*- coding: utf-8 -*-
from .models import Player
from prettytable import PrettyTable


def get_user_scores():
    table = PrettyTable()
    table.field_names = ["Gracz", "W", "P", "StrzB", "StraB", "% wyg", "Strzel/strac"]

    for p in Player.objects.all().order_by('-win_percent'):
        table.add_row([p.name, p.won_games, p.lost_games, p.won_point, p.lost_point, p.win_percent, p.win_lost_points_ratio])
    print(table)