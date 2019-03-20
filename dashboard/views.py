from django.shortcuts import render
from dashboard.models import Summoner
from dashboard.functions import *
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from dashboard.serializers import UserSerializer, SummonerSerializer, MatchSerializer, MatchPlayerSerializer
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests

def home(request):

    summonerCount = Summoner.objects.all().count()

    print(summonerCount)

    return render(request, 'dashboard/home.html', {
    'summonerCount': summonerCount,
    })

def summoners(request):
    if request.method == 'POST':
        if request.POST['action'] == 'fetchChallengers':
            fetch = fetchRiotAPI('OC1', 'league', 'v4', 'challengerleagues', 'by-queue', 'RANKED_SOLO_5x5')
            addSummoners(fetch, 'Challengers')
        elif request.POST['action'] == 'updateSummoner':
            updateSummoner(request.POST.get('puuid'))
        elif request.POST['action'] == 'addSummoner':
            addSummoners(request.POST.get('summonerName'), 'Summoner')

    return render(request, 'dashboard/summoners/summoners.html', {
    'summoners': Summoner.objects.all().order_by('-soloQ_leaguePoints'),
    })

def summonerDetails(request, summonerName):
    try:
        summoner = Summoner.objects.get(summonerName__iexact=summonerName)
    except Summoner.DoesNotExist:
        return HttpResponseRedirect('/digested')

    if request.POST.get('action', False) == 'updateSummoner':
        updateSummoner(summoner.puuid)
    elif request.POST.get('action', False) == 'fetchMatches':
        fetchMatches(summoner.puuid, 10)

    return render(request, 'dashboard/summoners/summonerDetails.html', {
    'summonerName': summonerName,
    })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def retrieve(self, request, pk=None):
        queryset = User.objects.filter(username=pk)
        user = get_object_or_404(queryset, pk=1)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)

class SummonerViewSet(viewsets.ModelViewSet):
    queryset = Summoner.objects.all().order_by('-soloQ_leaguePoints')
    serializer_class = SummonerSerializer

    def retrieve(self, request, pk=None):
        queryset = Summoner.objects.filter(summonerName__iexact=pk)
        print(queryset)
        summoner = get_object_or_404(queryset, summonerName__iexact=pk)
        serializer = SummonerSerializer(summoner, context={'request': request})
        return Response(serializer.data)

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('timestamp')
    serializer_class = MatchSerializer

    def retrieve(self, request, pk=None):
        queryset = Match.objects.filter(gameId=pk)
        match = get_object_or_404(queryset, gameId=pk)
        serializer = MatchSerializer(match, context={'request': request})
        return Response(serializer.data)

class MatchPlayerViewSet(viewsets.ModelViewSet):
    queryset = Match_Player.objects.all().order_by('match')
    serializer_class = MatchPlayerSerializer

    def retrieve(self, request, pk=None):
        queryset = Match_Player.objects.filter(summonerName__iexact=pk)
        serializer = MatchPlayerSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
