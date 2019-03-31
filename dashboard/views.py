from django.shortcuts import render
from dashboard.models import *
from dashboard.functions.general import *
from dashboard.functions.summoners import *
from dashboard.functions.champions import *
from django.contrib.auth import authenticate, login
from rest_framework import viewsets, generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from dashboard.serializers import *
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from colorama import Fore, Back, Style
from datetime import datetime
import requests

def home(request, reason=None):
    mySummoners = None
    summonerCount = Summoner.objects.all().count()

    # Sidebar Information
    isProfile = Profile.objects.all().filter(user=request.user) if request.user.is_authenticated == True else False

    if isProfile:
        profile = Profile.objects.get(user=request.user)
        mySummoners = Summoner.objects.filter(user_profile=profile)
    else:
        profile = None

    return render(request, 'dashboard/home.html', {
    'summonerCount': summonerCount,
    'profile': profile,
    'mySummoners': mySummoners,
    })

def summoners(request):
    mySummoners = None

    # Sidebar Information
    isProfile = Profile.objects.all().filter(user=request.user) if request.user.is_authenticated == True else False

    if isProfile:
        profile = Profile.objects.get(user=request.user)
        mySummoners = Summoner.objects.filter(user_profile=profile)
    else:
        profile = None

    return render(request, 'dashboard/summoners/summoners.html', {
    'summoners': Summoner.objects.all().order_by('-soloQ_leaguePoints'),
    'profile': profile,
    'mySummoners': mySummoners,
    })

def summonerDetails(request, summonerName):
    mySummoners = None
    functionResponse = None;

    # Sidebar Information
    isProfile = Profile.objects.all().filter(user=request.user) if request.user.is_authenticated == True else False

    if isProfile:
        profile = Profile.objects.get(user=request.user)
        mySummoners = Summoner.objects.filter(user_profile=profile)
    else:
        profile = None

    isSummoner = Summoner.objects.filter(summonerName__iexact=summonerName).count()
    if isSummoner == 1:
        summoner = Summoner.objects.get(summonerName__iexact=summonerName)
    else:
        return HttpResponseRedirect('/')

    return render(request, 'dashboard/summoners/summonerDetails.html', {
    'summonerName': summonerName,
    'profile': profile,
    'mySummoners': mySummoners,
    'functionResponse': functionResponse,
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
    queryset = Summoner.objects.all().order_by('summonerName')
    serializer_class = SummonerSerializer

    def get_queryset(self):
        queryset = Summoner.objects.all()
        tier = self.request.query_params.getlist('tier', None)
        if tier is not None:
            queryset = queryset.filter(soloQ_tier__in=tier).order_by('soloQ_tier','-soloQ_leaguePoints')
        return queryset

    def create(self, request):
        add = addSummoner(request.data['method'], request.data['value'])
        if add['isError'] != True:
            summoner = Summoner.objects.get(summonerId=add['summonerId'])
            update = updateSummoner(summoner.puuid)
            return JsonResponse(add, status=201)
        else:
            return JsonResponse(add)

    def retrieve(self, request, pk=None):
        # TODO: If no summoner is found by name, return error and display custom page.
        summoner = Summoner.objects.get(summonerName__iexact=pk)
        isUpdate = self.request.query_params.get('isUpdate')

        response = {}
        if isUpdate == 'True':
            updatedSummonerId = updateSummoner(summoner.puuid)
            latestMatches = fetchMatchList(summoner.puuid)
            if 'isError' in latestMatches:
                if latestMatches['isError']:
                    return JsonResponse(latestMatches)
            newMatches = []
            for match in latestMatches:
                existingMatch = Match.objects.filter(gameId=match['gameId'])
                if existingMatch.count() == 0:
                    match['timestamp'] = datetime.fromtimestamp(match['timestamp']/1000.)
                    newMatches.append(match)

            updatedSummoner = Summoner.objects.get(summonerId=updatedSummonerId)

            if updatedSummoner.summonerName != pk:
                return HttpResponseRedirect('/summoners/' + updatedSummoner.summonerName)
                
            serializer = SummonerSerializer(updatedSummoner, context={'request': request})
            response['newMatches'] = newMatches
            response['summonerInfo'] = serializer.data
            return Response(response)
        else:
            serializer = SummonerSerializer(summoner, context={'request': request})
            response['summonerInfo'] = serializer.data
            return Response(response)

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('timestamp')
    serializer_class = MatchListSerializer

    def create(self, request):
        existingMatch = Match.objects.filter(gameId=request.data['gameId'])
        if existingMatch.count() == 0:
            fetch = fetchMatch(request.data['gameId'])
            if fetch['ignore']:
                return Response(fetch)

            queryset = Match.objects.filter(gameId=request.data['gameId'])
            match = get_object_or_404(queryset, gameId=request.data['gameId'])
            serializer = MatchSerializer(match, context={'request': request})

            if match:
                matchClean = checkMatchIntegrity(match)

            response = {};
            response = fetch;
            response['newMatch'] = serializer.data;
            return Response(response)
        else:
            return Response('Existing game')

    def retrieve(self, request, pk=None):
        queryset = Match.objects.filter(gameId=pk)
        match = get_object_or_404(queryset, gameId=pk)
        serializer = MatchSerializer(match, context={'request': request})
        return Response(serializer.data)

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('match')
    serializer_class = MatchPlayerSerializer

    def get_queryset(self):
        queryset = Player.objects.all()
        matchId = self.request.query_params.get('match', None)
        summonerId = self.request.query_params.get('player', None)
        if matchId is not None and summonerId is not None:
            print(matchId)
            match = Match.objects.get(gameId=matchId)
            summoner = Summoner.objects.get(summonerId=summonerId)
            queryset = queryset.filter(match=match, summoner=summoner)
        return queryset

    def retrieve(self, request, pk=None):
        isSummoner = Summoner.objects.all().filter(summonerName__iexact=pk)
        if isSummoner != 0:
            summoner = Summoner.objects.get(summonerName__iexact=pk)
            queryset = Player.objects.filter(summoner=summoner.summonerId).order_by('match__gameId')
            serializer = MatchPlayerSerializer(queryset, many=True, context={'request': request})
            return Response(serializer.data)

class ChampionViewSet(viewsets.ModelViewSet):
    queryset = Champion.objects.all().order_by('champId')
    serializer_class = ChampionSerializer

    def create(self, request):
        isUpdate = request.data['isUpdate']
        if isUpdate == True:
            response = updateChampions('9.6.1')
        return Response(response)

    def retrieve(self, request, pk=None):
        queryset = Champion.objects.filter(champId__iexact=pk)
        serializer = ChampionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
