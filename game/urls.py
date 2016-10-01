# -*- coding: utf-8 -*-

from django.conf.urls import url

from game.views import TeamList, SlackTestView, TeamDetail, MatchDetail, MatchList

urlpatterns = [
    url(r'^teams/$', TeamList.as_view(), name='team-list'),
    url(r'^teams/(?P<pk>[\d]+)/$', TeamDetail.as_view(), name='team-detail'),
    url(r'^matches/$', MatchList.as_view(), name='match-list'),
    url(r'^matches/(?P<pk>[\d]+)/$', MatchDetail.as_view(), name='match-detail'),
    url(r'^slacktest/$', SlackTestView.as_view(), name='team-retrive-destroy')
]
