from dashboard.models import *
from dashboard.functions.general import *
from dashboard.functions.champions import *
from dashboard.functions.errors import *
from dashboard.functions.api import *
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core import serializers
from django.utils import timezone
from itertools import islice
from datetime import datetime
import requests, json

# Add Summoner Response:
# {'isError': False, 'errorMessage': '', 'summonerId': newSummoner.summonerId}


def addSummoner(method, value):
    if method == 'SummonerId':
        summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners/' + value)
    else:
        summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners/by-name/' + value)

    if 'status' in summonerInfo:
        print('[ERROR]: ' + summonerInfo['status']['message'] + '.')
        return {'isError': True, 'errorMessage': summonerInfo['status']['message'], 'summonerId': None}

    existingSummoner = Summoner.objects.filter(summonerId=summonerInfo['id'])

    if existingSummoner.count() == 0:

        try:
             newSummoner = Summoner.objects.create(
                # Ids
                summonerName=summonerInfo['name'],
                summonerId=summonerInfo['id'],
                puuid = summonerInfo['puuid'],
                accountId = summonerInfo['accountId'],

                # General
                server='OC1',
                profileIconId=summonerInfo['profileIconId'],
                summonerLevel=summonerInfo['summonerLevel'],

                # System
                date_created=timezone.now(),
            )
        except IntegrityError:
            existingSummoner = Summoner.objects.get(summonerId=summonerInfo['id'])
            return {'isError': True, 'errorMessage': 'Summoner already exists.', 'summonerId': newSummoner.summonerId}

        print('New Summoner Created: ' + newSummoner.summonerName)
        return {'isError': False, 'errorMessage': '', 'summonerId': newSummoner.summonerId}

    existingSummoner = Summoner.objects.get(summonerId=summonerInfo['id'])
    return {'isError': True, 'errorMessage': 'Summoner already exists.', 'summonerId': existingSummoner.summonerId}

def updateSummoner(puuid):
    summoner = Summoner.objects.get(puuid=puuid)
    print('Updating Summoner: ' + summoner.summonerName)

    summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners/by-puuid/' + puuid)
    if 'status' in summonerInfo:
        print('[ERROR]: ' + summonerInfo['status']['message'] + '.')
        return {'isError': True, 'errorMessage': summonerInfo['status']['message'] }

    summoner.summonerName = summonerInfo['name'] if summoner.summonerName != summonerInfo['name'] else summoner.summonerName
    summoner.profileIconId = summonerInfo['profileIconId'] if summoner.profileIconId != summonerInfo['profileIconId'] else summoner.profileIconId
    summoner.summonerLevel = summonerInfo['summonerLevel'] if summoner.summonerName != summonerInfo['summonerLevel'] else summoner.summonerName

    rankedInfo = fetchRiotAPI('OC1', 'league', 'v4', 'positions/by-summoner/' + summoner.summonerId)
    if 'status' in rankedInfo:
        print('[ERROR]: ' + rankedInfo['status']['message'] + '.')
        return {'isError': True, 'errorMessage': rankedInfo['status']['message'] }

    for queue in rankedInfo:
        if queue['queueType'] == 'RANKED_SOLO_5x5':
            soloQ = queue
            summoner.soloQ_leagueId = soloQ['leagueId'] if summoner.soloQ_leagueId != soloQ['leagueId'] else summoner.soloQ_leagueId
            summoner.soloQ_leagueName = soloQ['leagueName'] if summoner.soloQ_leagueName != soloQ['leagueName'] else summoner.soloQ_leagueName
            summoner.soloQ_tier = soloQ['tier'] if summoner.soloQ_tier != soloQ['tier'] else summoner.soloQ_tier
            summoner.soloQ_hotStreak = soloQ['hotStreak'] if summoner.soloQ_hotStreak != soloQ['hotStreak'] else summoner.soloQ_hotStreak
            summoner.soloQ_wins = soloQ['wins'] if summoner.soloQ_wins != soloQ['wins'] else summoner.soloQ_wins
            summoner.soloQ_losses = soloQ['losses'] if summoner.soloQ_losses != soloQ['losses'] else summoner.soloQ_losses
            summoner.soloQ_veteran = soloQ['veteran'] if summoner.soloQ_veteran != soloQ['veteran'] else summoner.soloQ_veteran
            summoner.soloQ_rank = soloQ['rank'] if summoner.soloQ_rank != soloQ['rank'] else summoner.soloQ_rank
            summoner.soloQ_inactive = soloQ['inactive'] if summoner.soloQ_inactive != soloQ['inactive'] else summoner.soloQ_inactive
            summoner.soloQ_freshBlood = soloQ['freshBlood'] if summoner.soloQ_freshBlood != soloQ['freshBlood'] else summoner.soloQ_freshBlood
            summoner.soloQ_leaguePoints = soloQ['leaguePoints'] if summoner.soloQ_leaguePoints != soloQ['leaguePoints'] else summoner.soloQ_leaguePoints

    summoner.date_updated = timezone.now()

    summoner.save()

    return JsonResponse({'message': 'Summoner Updated!','summonerName': summoner.summonerName, 'isError': False})
