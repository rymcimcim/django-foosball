# -*- coding: utf-8 -*-
from decimal import Decimal
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from game.helpers import FieldHistory
import game


class PlayerManager(BaseUserManager):
    def create_user(self, login, password, name=None):
        if not login:
            raise ValueError('Gracz musi mieć login')

        user = self.model(
            login=login,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password, name=None):
        user = self.create_user(
            login=login,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Player(AbstractBaseUser, FieldHistory):
    login = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    won_games = models.IntegerField(default=0)
    lost_games = models.IntegerField(default=0)
    tie_games = models.IntegerField(default=0)
    won_point = models.IntegerField(default=0)
    lost_point = models.IntegerField(default=0)

    # percent of won matches
    win_percent = models.DecimalField(default=0, max_digits=4, decimal_places=1)
    win_lost_points_ratio = models.DecimalField(default=0, max_digits=5, decimal_places=3)

    objects = PlayerManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name if self.name else self.login

    def get_short_name(self):
        return self.name if self.name else self.login

    def calculate_scores(self):
        self.won_games = 0
        self.lost_games = 0
        self.won_point = 0
        self.lost_point = 0

        for match in game.models.Match.objects.filter(team_2__players__id=self.id).prefetch_related('matchset_set'):
            if match.state == 'lost':
                self.won_games += 1
            elif match.state == 'win':
                self.lost_games += 1
            else:
                self.tie_games += 1
            self.won_point += match.get_team_2_total_points()
            self.lost_point += match.get_team_1_total_points()

        for match in game.models.Match.objects.filter(team_1__players__id=self.id).prefetch_related('matchset_set'):
            if match.state == 'win':
                self.won_games += 1
            elif match.state == 'lost':
                self.lost_games += 1
            else:
                self.tie_games += 1
            self.won_point += match.get_team_1_total_points()
            self.lost_point += match.get_team_2_total_points()

        self.win_percent = Decimal(self.won_games) / Decimal(self.won_games + self.lost_games + self.tie_games)
        self.win_lost_points_ratio = Decimal(self.won_point) / Decimal(self.lost_point)

        self.save()

    def __str__(self):              # __unicode__ on Python 2
        return self.login

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
