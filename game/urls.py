# -*- coding: utf-8 -*-

from django.conf.urls import url

from game.views import PlayersList, PlayersDetail, TeamList, TeamCreate, TeamRetriveDestroy

urlpatterns = [
    url(r'^players/$', PlayersList.as_view(), name='player-list'),
    url(r'^players/(?P<pk>[\d]+)/$', PlayersDetail.as_view(), name='player-detail'),
    url(r'^teams/$', TeamList.as_view(), name='team-list'),
    url(r'^teams/create/$', TeamCreate.as_view(), name='team-create'),
    url(r'^teams/(?P<pk>[\d]+)/$', TeamRetriveDestroy.as_view(), name='team-retrive-destroy')
]
