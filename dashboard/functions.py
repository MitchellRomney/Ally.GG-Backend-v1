from dashboard.models import Summoner, Match, Match_Team, Match_Player
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils import timezone
from itertools import islice
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
                newSummoner.soloQ_leagueId=rankedInfo[0]['leagueId']
                newSummoner.soloQ_leagueName=rankedInfo[0]['leagueName']
                newSummoner.soloQ_tier=rankedInfo[0]['tier']
                newSummoner.soloQ_hotStreak=rankedInfo[0]['hotStreak']
                newSummoner.soloQ_wins=rankedInfo[0]['wins']
                newSummoner.soloQ_losses=rankedInfo[0]['losses']
                newSummoner.soloQ_veteran=rankedInfo[0]['veteran']
                newSummoner.soloQ_rank=rankedInfo[0]['rank']
                newSummoner.soloQ_inactive=rankedInfo[0]['inactive']
                newSummoner.soloQ_freshBlood=rankedInfo[0]['freshBlood']
                newSummoner.soloQ_leaguePoints=rankedInfo[0]['leaguePoints']

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

def fetchMatches(puuid, amount):
    summoner = Summoner.objects.get(puuid=puuid)
    print('Fetching Summoner Matches: ' + summoner.summonerName)

    matches = fetchRiotAPI('OC1', 'match', 'v4', 'matchlists', 'by-account', summoner.accountId)
    for match in islice(matches['matches'], 0, 10):

        try:
            existingMatch = Match.objects.get(gameId=match['gameId'])
        except Match.DoesNotExist:
            print('Creating Match: ' + str(match['gameId']))

            matchInfo = fetchRiotAPI('OC1', 'match', 'v4', 'matches', match['gameId'])

            newMatch = Match(
                gameId = match['gameId'],
                platformId = match['platformId'],
                queueId = match['queue'],
                seasonId = match['season'],
                mapId = matchInfo['mapId'],

                gameMode = matchInfo['gameMode'],
                gameType = matchInfo['gameType'],
                gameVersion = matchInfo['gameVersion'],
                gameDuration = matchInfo['gameDuration'],
                timestamp = match['timestamp'],
            )

            newMatch.save()

            # Create the Teams

            for team in matchInfo['teams']:
                print(team)

                win = False if team['win'] == 'Fail' else True

                newTeam = Match_Team(
                    match = newMatch,

                    # General
                    win = win,
                    teamId = team['teamId'],

                    # Summoners Rift
                    firstDragon = team['firstDragon'],
                    firstInhibitor = team['firstInhibitor'],
                    firstRiftHerald = team['firstRiftHerald'],
                    firstBaron = team['firstBaron'],
                    baronKills = team['baronKills'],
                    riftHeraldKills = team['riftHeraldKills'],
                    firstBlood = team['firstBlood'],
                    firstTower = team['firstTower'],
                    inhibitorKills = team['inhibitorKills'],
                    towerKills = team['towerKills'],
                    dragonKills = team['dragonKills'],

                    # Other
                    dominionVictoryScore = team['dominionVictoryScore'],
                    vilemawKills = team['vilemawKills'],
                )

                newTeam.save()
                print('New Team Created - [' + str(newTeam) + ']')

            # Create the Player info for the match.
            for participantInfo in matchInfo['participantIdentities']:

                participantTeam = 100 if participantInfo['participantId'] <= 5 else 200

                for participant in matchInfo['participants']:
                    if participant['participantId'] == participantInfo['participantId']:
                        newPlayer = Match_Player(
                            # Key IDs & Participant Identity
                            match = newMatch,
                            currentPlatformId = participantInfo['player']['currentPlatformId'],
                            platformId = participantInfo['player']['platformId'],
                            matchHistoryUri = participantInfo['player']['matchHistoryUri'],
                            participantId = participantInfo['participantId'],
                            summonerName = participantInfo['player']['summonerName'],

                            teamId = participantTeam,

                            # General Player Information
                            spell1Id = participant['spell1Id'],
                            spell2Id = participant['spell2Id'],
                            championId = participant['championId'],

                            # Stats
                                ## Minions
                                totalMinionsKilled = participant['stats']['totalMinionsKilled'],
                                neutralMinionsKilled = participant['stats']['neutralMinionsKilled'],
                                neutralMinionsKilledTeamJungle = participant['stats']['neutralMinionsKilledTeamJungle'],
                                neutralMinionsKilledEnemyJungle = participant['stats']['neutralMinionsKilledEnemyJungle'],

                                ## Vision
                                visionScore = participant['stats']['visionScore'],
                                sightWardsBoughtInGame = participant['stats']['sightWardsBoughtInGame'],
                                visionWardsBoughtInGame = participant['stats']['visionWardsBoughtInGame'],
                                wardsKilled = participant['stats']['wardsKilled'],
                                wardsPlaced = participant['stats']['wardsPlaced'],

                                ## Damage Dealt
                                totalDamageDealt = participant['stats']['totalDamageDealt'],
                                totalDamageDealtToChampions = participant['stats']['totalDamageDealtToChampions'],
                                physicalDamageDealt = participant['stats']['physicalDamageDealt'],
                                physicalDamageDealtToChampions = participant['stats']['physicalDamageDealtToChampions'],
                                magicDamageDealt = participant['stats']['magicDamageDealt'],
                                magicDamageDealtToChampions = participant['stats']['magicDamageDealtToChampions'],
                                trueDamageDealt = participant['stats']['trueDamageDealt'],
                                trueDamageDealtToChampions = participant['stats']['trueDamageDealtToChampions'],
                                largestCriticalStrike = participant['stats']['largestCriticalStrike'],

                                ## Damage Taken
                                totalDamageTaken = participant['stats']['totalDamageTaken'],
                                physicalDamageTaken = participant['stats']['physicalDamageTaken'],
                                magicalDamageTaken = participant['stats']['magicalDamageTaken'],
                                trueDamageTaken = participant['stats']['trueDamageTaken'],
                                damageSelfMitigated = participant['stats']['damageSelfMitigated'],

                                # Objectives
                                turretKills = participant['stats']['turretKills'],
                                inhibitorKills = participant['stats']['inhibitorKills'],
                                damageDealtToTurrets = participant['stats']['damageDealtToTurrets'],
                                damageDealtToObjectives = participant['stats']['damageDealtToObjectives'],
                                firstInhibitorKill = participant['stats']['firstInhibitorKill'] if hasattr(participant['stats'], 'firstInhibitorKill') else False,
                                firstInhibitorAssist = participant['stats']['firstInhibitorAssist'] if hasattr(participant['stats'], 'firstInhibitorAssist') else False,
                                firstTowerAssist = participant['stats']['firstTowerAssist'] if hasattr(participant['stats'], 'firstTowerAssist') else False,
                                firstTowerKill = participant['stats']['firstTowerKill'] if hasattr(participant['stats'], 'firstTowerKill') else False,

                                ## Kills
                                kills = participant['stats']['kills'],
                                assists = participant['stats']['assists'],
                                killingSprees = participant['stats']['killingSprees'],
                                unrealKills = participant['stats']['unrealKills'],
                                doubleKills = participant['stats']['doubleKills'],
                                tripleKills = participant['stats']['tripleKills'],
                                quadraKills = participant['stats']['quadraKills'],
                                pentaKills = participant['stats']['pentaKills'],
                                largestMultiKill = participant['stats']['largestMultiKill'],
                                largestKillingSpree = participant['stats']['largestKillingSpree'],
                                firstBloodKill = participant['stats']['firstBloodKill'] if hasattr(participant['stats'], 'firstBloodKill') else False,
                                firstBloodAssist = participant['stats']['firstBloodAssist'] if hasattr(participant['stats'], 'firstBloodAssist') else False,

                                # Crowd Control
                                timeCCingOthers = participant['stats']['timeCCingOthers'],
                                totalTimeCrowdControlDealt = participant['stats']['totalTimeCrowdControlDealt'],

                                # Health
                                totalUnitsHealed = participant['stats']['totalUnitsHealed'],
                                totalHeal = participant['stats']['totalHeal'],
                                deaths = participant['stats']['deaths'],

                                # Perks
                                perk0 = participant['stats']['perk0'],
                                perk1 = participant['stats']['perk1'],
                                perk2 = participant['stats']['perk2'],
                                perk3 = participant['stats']['perk3'],
                                perk4 = participant['stats']['perk4'],
                                perk5 = participant['stats']['perk5'],
                                statPerk0 = participant['stats']['statPerk0'],
                                statPerk1 = participant['stats']['statPerk1'],
                                statPerk2 = participant['stats']['statPerk1'],
                                perk0Var1 = participant['stats']['perk0Var1'],
                                perk0Var2 = participant['stats']['perk0Var2'],
                                perk0Var3 = participant['stats']['perk0Var3'],
                                perk1Var1 = participant['stats']['perk1Var1'],
                                perk1Var2 = participant['stats']['perk1Var2'],
                                perk1Var3 = participant['stats']['perk1Var3'],
                                perk2Var1 = participant['stats']['perk2Var1'],
                                perk2Var2 = participant['stats']['perk2Var2'],
                                perk2Var3 = participant['stats']['perk2Var3'],
                                perk3Var1 = participant['stats']['perk3Var1'],
                                perk3Var2 = participant['stats']['perk3Var2'],
                                perk3Var3 = participant['stats']['perk3Var3'],
                                perk4Var1 = participant['stats']['perk4Var1'],
                                perk4Var2 = participant['stats']['perk4Var2'],
                                perk4Var3 = participant['stats']['perk4Var3'],
                                perk5Var1 = participant['stats']['perk5Var1'],
                                perk5Var2 = participant['stats']['perk5Var2'],
                                perk5Var3 = participant['stats']['perk5Var3'],
                                perkPrimaryStyle = participant['stats']['perkPrimaryStyle'],
                                perkSubStyle = participant['stats']['perkSubStyle'],

                                # Player Score
                                playerScore0 = participant['stats']['playerScore0'],
                                playerScore1 = participant['stats']['playerScore1'],
                                playerScore2 = participant['stats']['playerScore2'],
                                playerScore3 = participant['stats']['playerScore3'],
                                playerScore4 = participant['stats']['playerScore4'],
                                playerScore5 = participant['stats']['playerScore5'],
                                playerScore6 = participant['stats']['playerScore6'],
                                playerScore7 = participant['stats']['playerScore7'],
                                playerScore8 = participant['stats']['playerScore8'],
                                playerScore9 = participant['stats']['playerScore9'],
                                objectivePlayerScore = participant['stats']['objectivePlayerScore'],
                                combatPlayerScore = participant['stats']['combatPlayerScore'],
                                totalPlayerScore = participant['stats']['totalPlayerScore'],
                                totalScoreRank = participant['stats']['totalScoreRank'],

                                # Items
                                item0 = participant['stats']['item0'],
                                item1 = participant['stats']['item1'],
                                item2 = participant['stats']['item2'],
                                item3 = participant['stats']['item3'],
                                item4 = participant['stats']['item4'],
                                item5 = participant['stats']['item5'],
                                item6 = participant['stats']['item6'],

                                # Other
                                longestTimeSpentLiving = participant['stats']['longestTimeSpentLiving'],
                                goldEarned = participant['stats']['goldEarned'],
                                goldSpent = participant['stats']['goldSpent'],
                                win = participant['stats']['win'],
                                champLevel = participant['stats']['champLevel'],
                        )

                        newPlayer.save()
                        print('New Match Player Created: ' + newPlayer.summonerName)
