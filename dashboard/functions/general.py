from dashboard.models import *
from dashboard.functions.general import *
from dashboard.functions.champions import *
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from itertools import islice
from datetime import datetime
from colorama import Fore, Back, Style
import requests, json

def checkMatchIntegrity(match):
    players = Player.objects.filter(match=match)
    teams = Team.objects.filter(match=match)
    if players.count() != 10 or teams.count() != 2:
        # print('Match ' + str(match.gameId) + ' is missing ' + str(10-players.count()) + ' players.')
        match.delete()
        return False
    else:
        return True

def fetchMatchList(puuid):
    summoner = Summoner.objects.get(puuid=puuid)
    print(Fore.YELLOW + 'Fetching Summoner Matches: ' + Style.RESET_ALL + summoner.summonerName)

    matches = fetchRiotAPI('OC1', 'match', 'v4', 'matchlists/by-account/' + summoner.accountId, '?endIndex=10')
    if 'status' in matches:
        return {'isError': True, 'errorMessage': matches['status']['message'], 'ignore': False}

    return matches['matches']

def fetchMatch(gameId):
    existingMatchCount = Match.objects.filter(gameId=gameId).count()
    if existingMatchCount == 0:
        print(Fore.YELLOW + 'Building Match: ' + Style.RESET_ALL + str(gameId))

        matchInfo = fetchRiotAPI('OC1', 'match', 'v4', 'matches/' + str(gameId))

        if 'status' in matchInfo:
            print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL +     matchInfo['status']['message'] + '.')
            return {'isError': True, 'errorMessage': matchInfo['status']['message'], 'ignore': False}

        # TODO: Add functionality for Co-Op vs AI games.
        # Checking for Co-Op vs AI queue ID.
        if matchInfo['queueId'] == 850:
            print(Fore.CYAN + 'Match is Co-Op vs AI, skipping.' + Style.RESET_ALL)
            return {'isError': False, 'errorMessage': None, 'ignore': True}

        newMatch = Match.objects.create(
            gameId = matchInfo['gameId'],
            platformId = matchInfo['platformId'],
            queueId = matchInfo['queueId'],
            seasonId = matchInfo['seasonId'],
            mapId = matchInfo['mapId'],

            gameMode = matchInfo['gameMode'],
            gameType = matchInfo['gameType'],
            gameVersion = matchInfo['gameVersion'],
            gameDuration = matchInfo['gameDuration'],
            timestamp = matchInfo['gameCreation'],
        )

        for player in matchInfo['participantIdentities']:
            existingSummoner = Summoner.objects.filter(summonerId=player['player']['summonerId'])

            if existingSummoner.count() == 0:
                addResponse = addSummoner('SummonerId', player['player']['summonerId'])
                if addResponse['isError']: # If there is an error.
                    if addResponse['errorMessage'] == 'Summoner already exists.': # If that error is just that it already exists.
                        summoner = Summoner.objects.get(summonerId=player['player']['summonerId'])
                    else: # Else, serious error. Report it to the user.
                        return {'isError': True, 'errorMessage': addResponse['errorMessage'], 'ignore': False}
                else:
                    summoner = Summoner.objects.get(summonerId=player['player']['summonerId'])
            else:
                summoner = Summoner.objects.get(summonerId=player['player']['summonerId'])

            newMatch.players.add(summoner)

        # Create the Teams
        for team in matchInfo['teams']:

            win = False if team['win'] == 'Fail' else True

            newTeam = Team(
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
            print(Fore.GREEN + 'New Team Created:' + Style.RESET_ALL + str(newTeam))

        # Create the Player info for the match.
        for participantInfo in matchInfo['participantIdentities']:
            blueTeam = Team.objects.get(match=newMatch, teamId=100)
            redTeam = Team.objects.get(match=newMatch, teamId=200)
            participantTeam = blueTeam if participantInfo['participantId'] <= 5 else redTeam

            for participant in matchInfo['participants']:
                if participant['participantId'] == participantInfo['participantId']:

                    champion = Champion.objects.get(key=participant['championId'])

                    if existingSummoner.count() == 0:
                        addResponse = addSummoner('SummonerId', participantInfo['player']['summonerId'])
                        if addResponse['isError'] == True:
                            return {'isError': True, 'errorMessage': addResponse['errorMessage'], 'ignore': False}
                        else:
                            summoner = Summoner.objects.get(summonerId=participantInfo['player']['summonerId'])
                    else:
                        summoner = Summoner.objects.get(summonerId=participantInfo['player']['summonerId'])

                    newPlayer = Player(
                        # Key IDs & Participant Identity
                        match = newMatch,
                        currentPlatformId = participantInfo['player']['currentPlatformId'],
                        platformId = participantInfo['player']['platformId'],
                        matchHistoryUri = participantInfo['player']['matchHistoryUri'],
                        participantId = participantInfo['participantId'],
                        summoner = summoner,

                        team = participantTeam,

                        # General Player Information
                        spell1Id = participant['spell1Id'],
                        spell2Id = participant['spell2Id'],
                        champion = champion,

                        # Stats
                            ## Minions
                            totalMinionsKilled = participant['stats']['totalMinionsKilled'],
                            neutralMinionsKilled = participant['stats']['neutralMinionsKilled'],
                            neutralMinionsKilledTeamJungle = participant['stats']['neutralMinionsKilledTeamJungle'] if hasattr(participant['stats'], 'neutralMinionsKilledTeamJungle') else 0,
                            neutralMinionsKilledEnemyJungle = participant['stats']['neutralMinionsKilledEnemyJungle'] if hasattr(participant['stats'], 'neutralMinionsKilledEnemyJungle') else 0,

                            ## Vision
                            visionScore = participant['stats']['visionScore'],
                            sightWardsBoughtInGame = participant['stats']['sightWardsBoughtInGame'],
                            visionWardsBoughtInGame = participant['stats']['visionWardsBoughtInGame'],
                            wardsKilled = participant['stats']['wardsKilled'] if hasattr(participant['stats'], 'wardsKilled') else 0,
                            wardsPlaced = participant['stats']['wardsPlaced'] if hasattr(participant['stats'], 'wardsKilled') else 0,

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
                            perk0 = participant['stats']['perk0'] if hasattr(participant['stats'], 'perk0') else 0,
                            perk1 = participant['stats']['perk1'] if hasattr(participant['stats'], 'perk0') else 0,
                            perk2 = participant['stats']['perk2'] if hasattr(participant['stats'], 'perk0') else 0,
                            perk3 = participant['stats']['perk3'] if hasattr(participant['stats'], 'perk0') else 0,
                            perk4 = participant['stats']['perk4'] if hasattr(participant['stats'], 'perk0') else 0,
                            perk5 = participant['stats']['perk5'] if hasattr(participant['stats'], 'perk0') else 0,
                            statPerk0 = participant['stats']['statPerk0'] if hasattr(participant['stats'], 'statPerk0') else 0,
                            statPerk1 = participant['stats']['statPerk1'] if hasattr(participant['stats'], 'statPerk0') else 0,
                            statPerk2 = participant['stats']['statPerk1'] if hasattr(participant['stats'], 'statPerk0') else 0,
                            perk0Var1 = participant['stats']['perk0Var1'] if hasattr(participant['stats'], 'perk0Var1') else 0,
                            perk0Var2 = participant['stats']['perk0Var2'] if hasattr(participant['stats'], 'perk0Var2') else 0,
                            perk0Var3 = participant['stats']['perk0Var3'] if hasattr(participant['stats'], 'perk0Var3') else 0,
                            perk1Var1 = participant['stats']['perk1Var1'] if hasattr(participant['stats'], 'perk1Var1') else 0,
                            perk1Var2 = participant['stats']['perk1Var2'] if hasattr(participant['stats'], 'perk1Var2') else 0,
                            perk1Var3 = participant['stats']['perk1Var3'] if hasattr(participant['stats'], 'perk1Var3') else 0,
                            perk2Var1 = participant['stats']['perk2Var1'] if hasattr(participant['stats'], 'perk2Var1') else 0,
                            perk2Var2 = participant['stats']['perk2Var2'] if hasattr(participant['stats'], 'perk2Var2') else 0,
                            perk2Var3 = participant['stats']['perk2Var3'] if hasattr(participant['stats'], 'perk2Var3') else 0,
                            perk3Var1 = participant['stats']['perk3Var1'] if hasattr(participant['stats'], 'perk3Var1') else 0,
                            perk3Var2 = participant['stats']['perk3Var2'] if hasattr(participant['stats'], 'perk3Var2') else 0,
                            perk3Var3 = participant['stats']['perk3Var3'] if hasattr(participant['stats'], 'perk3Var3') else 0,
                            perk4Var1 = participant['stats']['perk4Var1'] if hasattr(participant['stats'], 'perk4Var1') else 0,
                            perk4Var2 = participant['stats']['perk4Var2'] if hasattr(participant['stats'], 'perk4Var2') else 0,
                            perk4Var3 = participant['stats']['perk4Var3'] if hasattr(participant['stats'], 'perk4Var3') else 0,
                            perk5Var1 = participant['stats']['perk5Var1'] if hasattr(participant['stats'], 'perk5Var1') else 0,
                            perk5Var2 = participant['stats']['perk5Var2'] if hasattr(participant['stats'], 'perk5Var2') else 0,
                            perk5Var3 = participant['stats']['perk5Var3'] if hasattr(participant['stats'], 'perk5Var3') else 0,
                            perkPrimaryStyle = participant['stats']['perkPrimaryStyle'] if hasattr(participant['stats'], 'perkPrimaryStyle') else 0,
                            perkSubStyle = participant['stats']['perkSubStyle'] if hasattr(participant['stats'], 'perkSubStyle') else 0,

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

                    print(Fore.GREEN + 'New Match Player Created: ' + Style.RESET_ALL + str(newPlayer.summoner))

    return {'isError': False, 'errorMessage': None, 'ignore': False}
