# -*- coding: utf-8 -*-

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from game.models import Team
from game.serializers import TeamSerializer, TeamCreateSerializer


class APIRoot(APIView):
    def get(self, request):
        return Response({
            'players': reverse('players:player-list', request=request),
            'teams-create': reverse('game:team-create', request=request),
            'teams': reverse('game:team-list', request=request),
        })


class TeamCreate(generics.CreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamCreateSerializer


class TeamList(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamRetriveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
