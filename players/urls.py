# -*- coding: utf-8 -*-

from django.conf.urls import url

from players.views import PlayersList, PlayersDetail

urlpatterns = [
    url(r'^$', PlayersList.as_view(), name='player-list'),
    url(r'^(?P<pk>[\d]+)/$', PlayersDetail.as_view(), name='player-detail')
]
