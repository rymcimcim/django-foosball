# -*- coding: utf-8 -*-

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from game.helpers import FieldHistory


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

    objects = PlayerManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return self.name if self.name else self.login

    def get_short_name(self):
        return self.name if self.name else self.login

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
