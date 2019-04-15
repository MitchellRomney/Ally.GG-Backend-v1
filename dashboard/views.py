from django.shortcuts import render
from dashboard.functions.general import *
from dashboard.functions.game_data import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from dashboard.serializers import *
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from datetime import datetime

globalSettings = Setting.objects.get(name='Global') if Setting.objects.filter(
    name='Global').count() == 1 else Setting.objects.create(name='Global', latestversion=get_latest_version())


def home(request):
    return render(request, 'dashboard/home.html', {
    })


def profile(request, username):
    user = User.objects.get(username=username) if User.objects.filter(username=username).count() == 1 else None
    profile = Profile.objects.get(user=user) if user else None
    return render(request, 'dashboard/profile.html', {
        'profile': profile,
    })


def summoners(request):
    return render(request, 'dashboard/summoners/summoners.html', {
        'summoners': Summoner.objects.all().order_by('-soloQ_leaguePoints'),
    })


def chat(request):
    return render(request, 'dashboard/chat.html', {

    })


def summonerDetails(request, summonerName):
    summoner = Summoner.objects.get(summonerName__iexact=summonerName) if Summoner.objects.filter(
        summonerName__iexact=summonerName).count() == 1 else None
    if summoner == None:
        # TODO: Display custom error page.
        return HttpResponseRedirect('/')

    return render(request, 'dashboard/summoners/summonerDetails.html', {
        'summoner': summoner,
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

    def get_queryset(self):
        queryset = Summoner.objects.all()
        tier = self.request.query_params.getlist('tier', None)
        order = self.request.query_params.get('order_by', None)
        if tier is not None:
            queryset = queryset.filter(soloQ_tier__in=tier).order_by('soloQ_tier', '-soloQ_leaguePoints')
        if order is not None:
            queryset = Summoner.objects.all().order_by('-' + order).exclude(**{order: None})
        return queryset

    def create(self, request):
        add = add_summoner(request.data['method'], request.data['value'])
        if add['isError'] != True:
            summoner = Summoner.objects.get(summonerId=add['summonerId'])
            update_summoner(summoner.puuid)
            return JsonResponse(add, status=201)
        else:
            return JsonResponse(add)

    def retrieve(self, request, pk=None):
        # TODO: If no summoner is found by name, return error and display custom page.
        summoner = Summoner.objects.get(summonerName__iexact=pk)
        isUpdate = self.request.query_params.get('isUpdate')

        response = {}
        if isUpdate == 'True':
            response = update_summoner(summoner.puuid)
            newSummonerId = response['summonerId']
            updatedSummoner = Summoner.objects.get(summonerId=newSummonerId)
            if updatedSummoner.summonerName.lower() != pk.lower():
                return HttpResponseRedirect('/summoners/' + updatedSummoner.summonerName)

            latestMatches = fetch_match_list(summoner.puuid)
            if 'isError' in latestMatches:
                if latestMatches['isError']:
                    return JsonResponse(latestMatches)
            newMatches = []
            for match in latestMatches:
                existingMatch = Match.objects.filter(gameId=match['gameId'])
                if existingMatch.count() == 0:
                    match['timestamp'] = datetime.fromtimestamp(match['timestamp'] / 1000.)
                    newMatches.append(match)

            serializer = SummonerSerializer(updatedSummoner, context={'request': request})
            response['newMatches'] = newMatches
            response['summonerInfo'] = serializer.data
            return Response(response)
        else:
            serializer = SummonerSerializer(summoner, context={'request': request})
            response['summonerInfo'] = serializer.data
            return Response(response)

    def get_serializer_class(self):
        tier = self.request.query_params.getlist('tier', None)
        if tier is not None:
            return MinimalSummonerSerializer
        return SummonerSerializer


class MatchViewSet(viewsets.ModelViewSet):
    serializer_class = MatchListSerializer
    queryset = Match.objects.all().order_by('timestamp')

    def get_queryset(self):
        queryset = Match.objects.all().order_by('timestamp')
        summoner = self.request.query_params.getlist('summoner', None)
        if summoner is not []:
            queryset = queryset.filter(Players__summoner__in=summoner).order_by('timestamp')[:10]
        return queryset

    def create(self, request):
        deleteAll = request.data['delete_all']
        if deleteAll == True:
            print('Deleting 5000 matches.')
            Match.objects.filter(pk__in=Match.objects.all().values_list('pk')[:10000]).delete()
            print('5000 Matches Deleted')
            return Response('All Matches Deleted')
        existingMatch = Match.objects.filter(gameId=request.data['gameId'])
        if existingMatch.count() == 0:
            fetch = fetch_match(request.data['gameId'])
            if fetch['ignore']:
                return Response(fetch)

            queryset = Match.objects.filter(gameId=request.data['gameId'])
            match = get_object_or_404(queryset, gameId=request.data['gameId'])
            serializer = MatchSerializer(match, context={'request': request})

            if match:
                check_match_integrity(match)

            response = fetch
            response['newMatch'] = serializer.data
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
            match = Match.objects.get(gameId=matchId)
            summoner = Summoner.objects.get(summonerId=summonerId)
            queryset = queryset.filter(match=match, summoner=summoner)
        return queryset

    def retrieve(self, request, pk=None):
        isSummoner = Summoner.objects.all().filter(summonerName__iexact=pk)
        if isSummoner != 0:
            minimal = self.request.query_params.get('minimal', None)
            summoner = Summoner.objects.get(summonerName__iexact=pk)
            queryset = Player.objects.filter(summoner=summoner.summonerId).order_by('-match__timestamp')
            serializer = MinimalPlayerSerializer(queryset, many=True,
                                                 context={'request': request}) if minimal else MatchPlayerSerializer(
                queryset, many=True, context={'request': request})
            return Response(serializer.data)


class GameView(APIView):
    def post(self, request):
        is_update = request.data['isUpdate']
        if is_update:
            response = update_game_data(globalSettings.latestVersion)
            return Response(response)
        return Response('Error, there is no endpoint here.')


class ChampionViewSet(viewsets.ModelViewSet):
    queryset = Champion.objects.all().order_by('champId')
    serializer_class = ChampionSerializer

    def retrieve(self, request, pk=None):
        queryset = Champion.objects.filter(champId__iexact=pk)
        serializer = ChampionSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all().order_by('-date_updated')
    serializer_class = ChatRoomSerializer

    def create(self, request):
        rooms = ChatRoom.objects.all()
        participants = [request.data['creator'], request.data['recipient']]
        for user in participants:
            rooms = rooms.filter(members__user__username=user)
        if rooms.count() == 1:
            room = rooms.get()
            print('Found Room! ' + str(room.roomId))
            # Redirect to room.
            return Response({'redirect': True, 'url': 'chat/'})
        # Create room, then redirect.

        creatorResponse = fetch_chatkit_api('users', request.data['creator'])
        print(creatorResponse)
        # Make GET request for both users, if user doesn't exist create it.
        # Make GET request for room that contains ONLY those 2 users, if doesn't exist create it.
        # Create Database object with the RoomID from the Room GET/POST and connect to the 2 user profiles.
        # return Response({'redirect': True, 'url': 'chat/'})
        return Response(True)

    def retrieve(self, request, pk=None):
        queryset = ChatRoom.objects.filter(members__user__username=pk)
        serializer = ChatRoomSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
