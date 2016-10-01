# -*- coding: utf-8 -*-

from django.conf.urls import url

from game.views import TeamList, TeamCreate, TeamRetriveDestroy

urlpatterns = [
    url(r'^teams/$', TeamList.as_view(), name='team-list'),
    url(r'^teams/create/$', TeamCreate.as_view(), name='team-create'),
    url(r'^teams/(?P<pk>[\d]+)/$', TeamRetriveDestroy.as_view(), name='team-retrive-destroy')
]
