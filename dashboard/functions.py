from dashboard.models import Summoner
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils import timezone
from datetime import datetime
import requests, json

def fetchRiotAPI(server, endpoint, version, option1, option2=None, option3=None):

    target = ''
    if (option2):
        target += '/' + str(option2)
    if (option3):
        target += '/' + str(option3)

    url = 'https://' + server + '.api.riotgames.com/lol/' + endpoint + '/' + version + '/' + option1 + target + '?api_key=' + settings.RIOT_API_KEY
    loadJson = json.loads(json.dumps(requests.get(url).json()))

    return loadJson

def addSummoners(summoners, context):
    currentSummoners = Summoner.objects.all().values_list('summonerId', flat=True)
    currentSummonersList = [summonerId for summonerId in currentSummoners]

    if context == 'Challengers':
        for summoner in summoners['entries']:
            print('Processing Summoner: ' + summoner['summonerName'])
            summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners', 'by-name', summoner['summonerName'])
            if summoner['summonerId'] in currentSummonersList:
                existingSummoner = Summoner.objects.get(puuid=summonerInfo['puuid'])
                if existingSummoner.date_updated < (timezone.now() - timezone.timedelta(minutes=10)):
                    try:
                        updateSummoner(summonerInfo['puuid'])
                        print('Summoner Updated.')
                    except:
                        print(summonerInfo)
                        break
                else:
                    print('Summoner Recently Updated, Skipping.')
            else:
                newSummoner = Summoner(
                    # Ids
                    summonerName=summoner['summonerName'],
                    summonerId=summoner['summonerId'],
                    puuid = summonerInfo['puuid'],
                    accountId = summonerInfo['accountId'],

                    # General
                    server='OC1',
                    profileIconId=summonerInfo['profileIconId'],
                    summonerLevel=summonerInfo['summonerLevel'],

                    # SoloQ
                    soloQ_leagueId=summoners['leagueId'],
                    soloQ_leagueName=summoners['name'],
                    soloQ_tier=summoners['tier'],
                    soloQ_hotStreak=summoner['hotStreak'],
                    soloQ_wins=summoner['wins'],
                    soloQ_losses=summoner['losses'],
                    soloQ_veteran=summoner['veteran'],
                    soloQ_rank=summoner['rank'],
                    soloQ_inactive=summoner['inactive'],
                    soloQ_freshBlood=summoner['freshBlood'],
                    soloQ_leaguePoints=summoner['leaguePoints'],

                    # System
                    date_created=timezone.now(),
                    date_updated=timezone.now(),
                )
                newSummoner.save()
                print('New Summoner Created.')

    if context == 'Summoner':
        try:
            existingSummoner = Summoner.objects.get(summonerName=summoners)
        except Summoner.DoesNotExist:
            summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners', 'by-name', summoners)
            print(summonerInfo)
            rankedInfo = fetchRiotAPI('OC1', 'league', 'v4', 'positions', 'by-summoner', summonerInfo['id'])
            print(rankedInfo)

            newSummoner = Summoner(
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
                date_updated=timezone.now(),
            )

            if rankedInfo != []:
                # SoloQ
                newSummoner.soloQ_leagueId=rankedInfo[0]['leagueId'],
                newSummoner.soloQ_leagueName=rankedInfo[0]['leagueName'],
                newSummoner.soloQ_tier=rankedInfo[0]['tier'],
                newSummoner.soloQ_hotStreak=rankedInfo[0]['hotStreak'],
                newSummoner.soloQ_wins=rankedInfo[0]['wins'],
                newSummoner.soloQ_losses=rankedInfo[0]['losses'],
                newSummoner.soloQ_veteran=rankedInfo[0]['veteran'],
                newSummoner.soloQ_rank=rankedInfo[0]['rank'],
                newSummoner.soloQ_inactive=rankedInfo[0]['inactive'],
                newSummoner.soloQ_freshBlood=rankedInfo[0]['freshBlood'],
                newSummoner.soloQ_leaguePoints=rankedInfo[0]['leaguePoints'],
                
            newSummoner.save()
            print('New Summoner Created.')

def updateSummoner(puuid):
    summoner = Summoner.objects.get(puuid=puuid)
    print('Updating Summoner: ' + summoner.summonerName)

    summonerInfo = fetchRiotAPI('OC1', 'summoner', 'v4', 'summoners', 'by-puuid', puuid)
    summoner.summonerName = summonerInfo['name'] if summoner.summonerName != summonerInfo['name'] else summoner.summonerName
    summoner.profileIconId = summonerInfo['profileIconId'] if summoner.profileIconId != summonerInfo['profileIconId'] else summoner.profileIconId
    summoner.summonerLevel = summonerInfo['summonerLevel'] if summoner.summonerName != summonerInfo['summonerLevel'] else summoner.summonerName

    rankedInfo = fetchRiotAPI('OC1', 'league', 'v4', 'positions', 'by-summoner', summoner.summonerId)
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
