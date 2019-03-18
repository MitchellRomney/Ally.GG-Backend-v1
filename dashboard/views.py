from django.shortcuts import render
from dashboard.models import Summoner
from dashboard.functions import *
from django.contrib.auth import authenticate, login
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from dashboard.serializers import UserSerializer, SummonerSerializer
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import requests

def home(request):
    if not request.user.is_authenticated:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return render(request, 'dashboard/home.html')
    else:
        if request.method == 'POST':
            if request.POST['action'] == 'fetchChallengers':
                fetch = fetchRiotAPI('OC1', 'league', 'v4', 'challengerleagues', 'by-queue', 'RANKED_SOLO_5x5')
                addSummoners(fetch, 'Challengers')
            elif request.POST['action'] == 'updateSummoner':
                updateSummoner(request.POST.get('puuid'))
            elif request.POST['action'] == 'addSummoner':
                addSummoners(request.POST.get('summonerName'), 'Summoner')

        return render(request, 'dashboard/home.html', {
        'summoners': Summoner.objects.all().order_by('-soloQ_leaguePoints'),
        })

def summonerDetails(request, summonerName):
    try:
        summoner = Summoner.objects.get(summonerName=summonerName)
    except Summoner.DoesNotExist:
        return HttpResponseRedirect('/digested')

    print(summonerName)

    return render(request, 'leaguedigested/summonerDetails.html', {
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
        queryset = Summoner.objects.filter(summonerName=pk)
        summoner = get_object_or_404(queryset, summonerName=pk)
        serializer = SummonerSerializer(summoner, context={'request': request})
        return Response(serializer.data)
