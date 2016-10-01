# -*- coding: utf-8 -*-

from rest_framework import serializers

from game.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = ['password', 'is_active', 'is_admin']
