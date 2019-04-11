from dashboard.models import *
from dashboard.functions.general import *
from dashboard.functions.champions import *
from dashboard.functions.errors import *
from dashboard.functions.api import *
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.core import serializers
from django.utils import timezone
from django.db import IntegrityError
from itertools import islice
from datetime import datetime
from colorama import Fore, Back, Style
import requests, json

# Add Summoner Response:
# {'isError': False, 'errorMessage': '', 'summonerId': newSummoner.summonerId}


def addSummoner(method, value):
    if method == 'SummonerId':
        summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners/' + value)
    else:
        summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners/by-name/' + value)

    if 'status' in summonerInfo:
        print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + summonerInfo['status']['message'] + '.')
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

        print(Fore.GREEN + 'New Summoner Created: ' + Style.RESET_ALL + newSummoner.summonerName)
        return {'isError': False, 'errorMessage': '', 'summonerId': newSummoner.summonerId}

    existingSummoner = Summoner.objects.get(summonerId=summonerInfo['id'])
    return {'isError': True, 'errorMessage': 'Summoner already exists.', 'summonerId': existingSummoner.summonerId}

def updateSummoner(puuid):
    summoner = Summoner.objects.get(puuid=puuid)
    print(Fore.YELLOW + 'Updating Summoner: ' + Style.RESET_ALL + summoner.summonerName)

    summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners/by-puuid/' + puuid)
    if 'status' in summonerInfo:
        print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + summonerInfo['status']['message'] + '.')
        return {'isError': True, 'errorMessage': summonerInfo['status']['message'] }

    summoner.summonerName = summonerInfo['name'] if summoner.summonerName != summonerInfo['name'] else summoner.summonerName
    summoner.profileIconId = summonerInfo['profileIconId'] if summoner.profileIconId != summonerInfo['profileIconId'] else summoner.profileIconId
    summoner.summonerLevel = summonerInfo['summonerLevel'] if summoner.summonerName != summonerInfo['summonerLevel'] else summoner.summonerName

    rankedInfo = fetchRiotAPI('OC1', 'league', 'v4', 'positions/by-summoner/' + summoner.summonerId)
    if 'status' in rankedInfo:
        print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + rankedInfo['status']['message'] + '.')
        return {'isError': True, 'errorMessage': rankedInfo['status']['message'] }

    for queue in rankedInfo:
        if queue['queueType'] == 'RANKED_SOLO_5x5':
            summoner.soloQ_leagueId = queue['leagueId'] if summoner.soloQ_leagueId != queue['leagueId'] else summoner.soloQ_leagueId
            summoner.soloQ_leagueName = soloQ['leagueName'] if summoner.soloQ_leagueName != queue['leagueName'] else summoner.soloQ_leagueName
            summoner.soloQ_tier = queue['tier'] if summoner.soloQ_tier != queue['tier'] else summoner.soloQ_tier
            summoner.soloQ_hotStreak = queue['hotStreak'] if summoner.soloQ_hotStreak != queue['hotStreak'] else summoner.soloQ_hotStreak
            summoner.soloQ_wins = queue['wins'] if summoner.soloQ_wins != queue['wins'] else summoner.soloQ_wins
            summoner.soloQ_losses = queue['losses'] if summoner.soloQ_losses != queue['losses'] else summoner.soloQ_losses
            summoner.soloQ_veteran = queue['veteran'] if summoner.soloQ_veteran != queue['veteran'] else summoner.soloQ_veteran
            summoner.soloQ_rank = queue['rank'] if summoner.soloQ_rank != queue['rank'] else summoner.soloQ_rank
            summoner.soloQ_inactive = queue['inactive'] if summoner.soloQ_inactive != queue['inactive'] else summoner.soloQ_inactive
            summoner.soloQ_freshBlood = queue['freshBlood'] if summoner.soloQ_freshBlood != queue['freshBlood'] else summoner.soloQ_freshBlood
            summoner.soloQ_leaguePoints = queue['leaguePoints'] if summoner.soloQ_leaguePoints != queue['leaguePoints'] else summoner.soloQ_leaguePoints
        if queue['queueType'] == 'RANKED_FLEX_SR':
            summoner.flexSR_leagueId = queue['leagueId'] if summoner.flexSR_leagueId != queue['leagueId'] else summoner.flexSR_leagueId
            summoner.flexSR_leagueName = queue['leagueName'] if summoner.flexSR_leagueName != queue['leagueName'] else summoner.flexSR_leagueName
            summoner.flexSR_tier = queue['tier'] if summoner.flexSR_tier != queue['tier'] else summoner.flexSR_tier
            summoner.flexSR_hotStreak = queue['hotStreak'] if summoner.flexSR_hotStreak != queue['hotStreak'] else summoner.flexSR_hotStreak
            summoner.flexSR_wins = queue['wins'] if summoner.flexSR_wins != queue['wins'] else summoner.flexSR_wins
            summoner.flexSR_losses = queue['losses'] if summoner.flexSR_losses != queue['losses'] else summoner.flexSR_losses
            summoner.flexSR_veteran = queue['veteran'] if summoner.flexSR_veteran != queue['veteran'] else summoner.flexSR_veteran
            summoner.flexSR_rank = queue['rank'] if summoner.flexSR_rank != queue['rank'] else summoner.flexSR_rank
            summoner.flexSR_inactive = queue['inactive'] if summoner.flexSR_inactive != queue['inactive'] else summoner.flexSR_inactive
            summoner.flexSR_freshBlood = queue['freshBlood'] if summoner.flexSR_freshBlood != queue['freshBlood'] else summoner.flexSR_freshBlood
            summoner.flexSR_leaguePoints = queue['leaguePoints'] if summoner.flexSR_leaguePoints != queue['leaguePoints'] else summoner.flexSR_leaguePoints
        if queue['queueType'] == 'RANKED_FLEX_TT':
            summoner.flexTT_leagueId = queue['leagueId'] if summoner.flexTT_leagueId != queue['leagueId'] else summoner.flexTT_leagueId
            summoner.flexTT_leagueName = queue['leagueName'] if summoner.flexTT_leagueName != queue['leagueName'] else summoner.flexTT_leagueName
            summoner.flexTT_tier = queue['tier'] if summoner.flexTT_tier != queue['tier'] else summoner.flexTT_tier
            summoner.flexTT_hotStreak = queue['hotStreak'] if summoner.flexTT_hotStreak != queue['hotStreak'] else summoner.flexTT_hotStreak
            summoner.flexTT_wins = queue['wins'] if summoner.flexTT_wins != queue['wins'] else summoner.flexTT_wins
            summoner.flexTT_losses = queue['losses'] if summoner.flexTT_losses != queue['losses'] else summoner.flexTT_losses
            summoner.flexTT_veteran = queue['veteran'] if summoner.flexTT_veteran != queue['veteran'] else summoner.flexTT_veteran
            summoner.flexTT_rank = queue['rank'] if summoner.flexTT_rank != queue['rank'] else summoner.flexTT_rank
            summoner.flexTT_inactive = queue['inactive'] if summoner.flexTT_inactive != queue['inactive'] else summoner.flexTT_inactive
            summoner.flexTT_freshBlood = queue['freshBlood'] if summoner.flexTT_freshBlood != queue['freshBlood'] else summoner.flexTT_freshBlood
            summoner.flexTT_leaguePoints = queue['leaguePoints'] if summoner.flexTT_leaguePoints != queue['leaguePoints'] else summoner.flexTT_leaguePoints

    summoner.date_updated = timezone.now()

    summoner.save()

    return {'message': 'Summoner Updated!','summonerId': summoner.summonerId, 'isError': False}
