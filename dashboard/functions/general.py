from dashboard.functions.game_data import *
from sentry_sdk import capture_exception, configure_scope
from datetime import datetime
from colorama import Fore, Style
import requests
import json
import re
import pytz


def get_latest_version():
    version_list = json.loads(json.dumps(requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()))
    print(Fore.MAGENTA + '[DDRAGON API]: ' + Style.RESET_ALL + 'https://ddragon.leagueoflegends.com/api/versions.json')
    return version_list[0]


def check_match_integrity(match):
    players = Player.objects.filter(match=match)
    teams = Team.objects.filter(match=match)
    if players.count() != 10 or teams.count() != 2:
        match.delete()
        return False
    else:
        return True


def fetch_match_list(summoner_id):
    summoner = Summoner.objects.get(summonerId=summoner_id)
    matches = fetch_riot_api('OC1', 'match', 'v4', 'matchlists/by-account/' + summoner.accountId, '?endIndex=10')
    if 'matches' in matches:
        return matches['matches']
    else:
        return []


def fetch_match(game_id):
    if Match.objects.filter(gameId=game_id).count() == 0:

        match_info = fetch_riot_api('OC1', 'match', 'v4', 'matches/' + str(game_id))

        patch = re.compile('\d\.\d{1,2}\.').findall(match_info["gameVersion"])[0] + '1'

        timestamp = datetime.utcfromtimestamp(match_info['gameCreation'] / 1000.).replace(tzinfo=pytz.UTC)

        if Match.objects.filter(gameId=game_id).count() == 0 and match_info['seasonId'] >= 10:
            new_match = Match.objects.create(
                gameId=match_info['gameId'],
                platformId=match_info['platformId'],
                queueId=match_info['queueId'],
                seasonId=match_info['seasonId'],
                mapId=match_info['mapId'],

                gameMode=match_info['gameMode'],
                gameType=match_info['gameType'],
                gameVersion=match_info['gameVersion'],
                gameDuration=match_info['gameDuration'],
                timestamp=timestamp,
            )

            for player in match_info['participantIdentities']:
                if player['player']['accountId'] != '0':
                    if Summoner.objects.filter(summonerId=player['player']['summonerId']).count() == 0:
                        add_summoner('SummonerId', player['player']['summonerId'])
                    new_match.players.add(Summoner.objects.get(summonerId=player['player']['summonerId']))
                else:
                    new_match.bots.add(Champion.objects.get(champId__iexact=player['player']['summonerName']))

            # Create the Teams
            for team in match_info['teams']:
                win = False if team['win'] == 'Fail' else True

                new_team = Team(
                    match=new_match,

                    # General
                    win=win,
                    teamId=team['teamId'],

                    # Summoners Rift
                    firstDragon=team['firstDragon'],
                    firstInhibitor=team['firstInhibitor'],
                    firstRiftHerald=team['firstRiftHerald'],
                    firstBaron=team['firstBaron'],
                    baronKills=team['baronKills'],
                    riftHeraldKills=team['riftHeraldKills'],
                    firstBlood=team['firstBlood'],
                    firstTower=team['firstTower'],
                    inhibitorKills=team['inhibitorKills'],
                    towerKills=team['towerKills'],
                    dragonKills=team['dragonKills'],

                    # Other
                    dominionVictoryScore=team['dominionVictoryScore'],
                    vilemawKills=team['vilemawKills'],
                )

                new_team.save()
                # print(Fore.GREEN + 'New Team Created:' + Style.RESET_ALL + str(new_team))

            # Create the Player info for the match.
            for participant_info in match_info['participantIdentities']:
                blue_team = Team.objects.get(match=new_match, teamId=100)
                red_team = Team.objects.get(match=new_match, teamId=200)
                participant_team = blue_team if participant_info['participantId'] <= 5 else red_team

                for participant in match_info['participants']:
                    if participant['participantId'] == participant_info['participantId']:
                        if Match.objects.filter(gameId=match_info['gameId']).count() != 0:
                            try:
                                new_player = Player(
                                    # Key IDs & Participant Identity
                                    match=Match.objects.get(gameId=match_info['gameId']),
                                    currentPlatformId=participant_info['player']['currentPlatformId'],
                                    platformId=participant_info['player']['platformId'],
                                    matchHistoryUri=participant_info['player']['matchHistoryUri'],
                                    participantId=participant_info['participantId'],
                                    summoner=Summoner.objects.get(summonerId=participant_info['player']['summonerId'])
                                    if 'summonerId' in participant_info['player'] else None,

                                    team=participant_team,

                                    # General Player Information
                                    spell1Id=SummonerSpell.objects.get(key=participant['spell1Id']),
                                    spell2Id=SummonerSpell.objects.get(key=participant['spell2Id']),
                                    champion=Champion.objects.get(key=participant['championId']),

                                    # Minions
                                    totalMinionsKilled=participant['stats']['totalMinionsKilled'],
                                    neutralMinionsKilled=participant['stats']['neutralMinionsKilled'],
                                    neutralMinionsKilledTeamJungle=participant['stats'][
                                        'neutralMinionsKilledTeamJungle'] if 'neutralMinionsKilledTeamJungle' in participant[
                                        'stats'] else 0,
                                    neutralMinionsKilledEnemyJungle=participant['stats'][
                                        'neutralMinionsKilledEnemyJungle'] if 'neutralMinionsKilledEnemyJungle' in participant[
                                        'stats'] else 0,

                                    # Vision
                                    visionScore=participant['stats']['visionScore'],
                                    sightWardsBoughtInGame=participant['stats']['sightWardsBoughtInGame'],
                                    visionWardsBoughtInGame=participant['stats']['visionWardsBoughtInGame'],
                                    wardsKilled=participant['stats']['wardsKilled'] if 'wardsKilled' in participant['stats'] else 0,
                                    wardsPlaced=participant['stats']['wardsPlaced'] if 'wardsKilled' in participant['stats'] else 0,

                                    # Damage Dealt
                                    totalDamageDealt=participant['stats']['totalDamageDealt'],
                                    totalDamageDealtToChampions=participant['stats']['totalDamageDealtToChampions'],
                                    physicalDamageDealt=participant['stats']['physicalDamageDealt'],
                                    physicalDamageDealtToChampions=participant['stats']['physicalDamageDealtToChampions'],
                                    magicDamageDealt=participant['stats']['magicDamageDealt'],
                                    magicDamageDealtToChampions=participant['stats']['magicDamageDealtToChampions'],
                                    trueDamageDealt=participant['stats']['trueDamageDealt'],
                                    trueDamageDealtToChampions=participant['stats']['trueDamageDealtToChampions'],
                                    largestCriticalStrike=participant['stats']['largestCriticalStrike'],

                                    # Damage Taken
                                    totalDamageTaken=participant['stats']['totalDamageTaken'],
                                    physicalDamageTaken=participant['stats']['physicalDamageTaken'],
                                    magicalDamageTaken=participant['stats']['magicalDamageTaken'],
                                    trueDamageTaken=participant['stats']['trueDamageTaken'],
                                    damageSelfMitigated=participant['stats']['damageSelfMitigated'],

                                    # Objectives
                                    turretKills=participant['stats']['turretKills'],
                                    inhibitorKills=participant['stats']['inhibitorKills'],
                                    damageDealtToTurrets=participant['stats']['damageDealtToTurrets'],
                                    damageDealtToObjectives=participant['stats']['damageDealtToObjectives'],
                                    firstInhibitorKill=participant['stats']['firstInhibitorKill'] if 'firstInhibitorKill' in
                                                                                                     participant[
                                                                                                         'stats'] else False,
                                    firstInhibitorAssist=participant['stats']['firstInhibitorAssist'] if 'firstInhibitorAssist' in
                                                                                                         participant[
                                                                                                             'stats'] else False,
                                    firstTowerAssist=participant['stats']['firstTowerAssist'] if 'firstTowerAssist' in participant[
                                        'stats'] else False,
                                    firstTowerKill=participant['stats']['firstTowerKill'] if 'firstTowerKill' in participant[
                                        'stats'] else False,

                                    # Kills
                                    kills=participant['stats']['kills'],
                                    assists=participant['stats']['assists'],
                                    killingSprees=participant['stats']['killingSprees'],
                                    unrealKills=participant['stats']['unrealKills'],
                                    doubleKills=participant['stats']['doubleKills'],
                                    tripleKills=participant['stats']['tripleKills'],
                                    quadraKills=participant['stats']['quadraKills'],
                                    pentaKills=participant['stats']['pentaKills'],
                                    largestMultiKill=participant['stats']['largestMultiKill'],
                                    largestKillingSpree=participant['stats']['largestKillingSpree'],
                                    firstBloodKill=participant['stats']['firstBloodKill'] if 'firstBloodKill' in participant[
                                        'stats'] else False,
                                    firstBloodAssist=participant['stats']['firstBloodAssist'] if 'firstBloodAssist' in participant[
                                        'stats'] else False,

                                    # Crowd Control
                                    timeCCingOthers=participant['stats']['timeCCingOthers'],
                                    totalTimeCrowdControlDealt=participant['stats']['totalTimeCrowdControlDealt'],

                                    # Health
                                    totalUnitsHealed=participant['stats']['totalUnitsHealed'],
                                    totalHeal=participant['stats']['totalHeal'],
                                    deaths=participant['stats']['deaths'],

                                    # Perks
                                    statPerk0=participant['stats']['statPerk0'] if 'statPerk0' in participant['stats'] else 0,
                                    statPerk1=participant['stats']['statPerk1'] if 'statPerk0' in participant['stats'] else 0,
                                    statPerk2=participant['stats']['statPerk1'] if 'statPerk0' in participant['stats'] else 0,
                                    perk0Var1=participant['stats']['perk0Var1'] if 'perk0Var1' in participant['stats'] else 0,
                                    perk0Var2=participant['stats']['perk0Var2'] if 'perk0Var2' in participant['stats'] else 0,
                                    perk0Var3=participant['stats']['perk0Var3'] if 'perk0Var3' in participant['stats'] else 0,
                                    perk1Var1=participant['stats']['perk1Var1'] if 'perk1Var1' in participant['stats'] else 0,
                                    perk1Var2=participant['stats']['perk1Var2'] if 'perk1Var2' in participant['stats'] else 0,
                                    perk1Var3=participant['stats']['perk1Var3'] if 'perk1Var3' in participant['stats'] else 0,
                                    perk2Var1=participant['stats']['perk2Var1'] if 'perk2Var1' in participant['stats'] else 0,
                                    perk2Var2=participant['stats']['perk2Var2'] if 'perk2Var2' in participant['stats'] else 0,
                                    perk2Var3=participant['stats']['perk2Var3'] if 'perk2Var3' in participant['stats'] else 0,
                                    perk3Var1=participant['stats']['perk3Var1'] if 'perk3Var1' in participant['stats'] else 0,
                                    perk3Var2=participant['stats']['perk3Var2'] if 'perk3Var2' in participant['stats'] else 0,
                                    perk3Var3=participant['stats']['perk3Var3'] if 'perk3Var3' in participant['stats'] else 0,
                                    perk4Var1=participant['stats']['perk4Var1'] if 'perk4Var1' in participant['stats'] else 0,
                                    perk4Var2=participant['stats']['perk4Var2'] if 'perk4Var2' in participant['stats'] else 0,
                                    perk4Var3=participant['stats']['perk4Var3'] if 'perk4Var3' in participant['stats'] else 0,
                                    perk5Var1=participant['stats']['perk5Var1'] if 'perk5Var1' in participant['stats'] else 0,
                                    perk5Var2=participant['stats']['perk5Var2'] if 'perk5Var2' in participant['stats'] else 0,
                                    perk5Var3=participant['stats']['perk5Var3'] if 'perk5Var3' in participant['stats'] else 0,
                                    perkPrimaryStyle=participant['stats']['perkPrimaryStyle'] if 'perkPrimaryStyle' in participant[
                                        'stats'] else 0,
                                    perkSubStyle=participant['stats']['perkSubStyle'] if 'perkSubStyle' in participant[
                                        'stats'] else 0,

                                    # Player Score
                                    playerScore0=participant['stats']['playerScore0'],
                                    playerScore1=participant['stats']['playerScore1'],
                                    playerScore2=participant['stats']['playerScore2'],
                                    playerScore3=participant['stats']['playerScore3'],
                                    playerScore4=participant['stats']['playerScore4'],
                                    playerScore5=participant['stats']['playerScore5'],
                                    playerScore6=participant['stats']['playerScore6'],
                                    playerScore7=participant['stats']['playerScore7'],
                                    playerScore8=participant['stats']['playerScore8'],
                                    playerScore9=participant['stats']['playerScore9'],
                                    objectivePlayerScore=participant['stats']['objectivePlayerScore'],
                                    combatPlayerScore=participant['stats']['combatPlayerScore'],
                                    totalPlayerScore=participant['stats']['totalPlayerScore'],
                                    totalScoreRank=participant['stats']['totalScoreRank'],

                                    # Other
                                    longestTimeSpentLiving=participant['stats']['longestTimeSpentLiving'],
                                    goldEarned=participant['stats']['goldEarned'],
                                    goldSpent=participant['stats']['goldSpent'],
                                    win=participant['stats']['win'],
                                    champLevel=participant['stats']['champLevel'],
                                )

                                # Items
                                if Item.objects.filter(itemId=participant['stats']['item0']).count() != 0:
                                    new_player.item0 = Item.objects.get(itemId=participant['stats']['item0'])
                                else:
                                    check_items(patch)
                                    new_player.item0 = Item.objects.get(itemId=participant['stats']['item0'])

                                if Item.objects.filter(itemId=participant['stats']['item1']).count() != 0:
                                    new_player.item1 = Item.objects.get(itemId=participant['stats']['item1'])
                                else:
                                    check_items(patch)
                                    new_player.item1 = Item.objects.get(itemId=participant['stats']['item1'])

                                if Item.objects.filter(itemId=participant['stats']['item2']).count() != 0:
                                    new_player.item2 = Item.objects.get(itemId=participant['stats']['item2'])
                                else:
                                    check_items(patch)
                                    new_player.item2 = Item.objects.get(itemId=participant['stats']['item2'])

                                if Item.objects.filter(itemId=participant['stats']['item3']).count() != 0:
                                    new_player.item3 = Item.objects.get(itemId=participant['stats']['item3'])
                                else:
                                    check_items(patch)
                                    new_player.item3 = Item.objects.get(itemId=participant['stats']['item3'])

                                if Item.objects.filter(itemId=participant['stats']['item4']).count() != 0:
                                    new_player.item4 = Item.objects.get(itemId=participant['stats']['item4'])
                                else:
                                    check_items(patch)
                                    new_player.item4 = Item.objects.get(itemId=participant['stats']['item4'])

                                if Item.objects.filter(itemId=participant['stats']['item5']).count() != 0:
                                    new_player.item5 = Item.objects.get(itemId=participant['stats']['item5'])
                                else:
                                    check_items(patch)
                                    new_player.item5 = Item.objects.get(itemId=participant['stats']['item5'])

                                if Item.objects.filter(itemId=participant['stats']['item6']).count() != 0:
                                    new_player.item6 = Item.objects.get(itemId=participant['stats']['item6'])
                                else:
                                    check_items(patch)
                                    new_player.item6 = Item.objects.get(itemId=participant['stats']['item6'])

                                if 'perk0' in participant['stats']:
                                    if Rune.objects.filter(runeId=participant['stats']['perk0']).count() != 0:
                                        new_player.perk0 = Rune.objects.get(runeId=participant['stats']['perk0'])
                                    else:
                                        check_runes(patch)
                                        new_player.perk0 = Rune.objects.get(runeId=participant['stats']['perk0'])

                                if 'perk1' in participant['stats']:
                                    if Rune.objects.filter(runeId=participant['stats']['perk1']).count() != 0:
                                        new_player.perk1 = Rune.objects.get(runeId=participant['stats']['perk1'])
                                    else:
                                        check_runes(patch)
                                        new_player.perk1 = Rune.objects.get(runeId=participant['stats']['perk1'])

                                if 'perk2' in participant['stats']:
                                    if Rune.objects.filter(runeId=participant['stats']['perk2']).count() != 0:
                                        new_player.perk2 = Rune.objects.get(runeId=participant['stats']['perk2'])
                                    else:
                                        check_runes(patch)
                                        new_player.perk2 = Rune.objects.get(runeId=participant['stats']['perk2'])

                                if 'perk3' in participant['stats']:
                                    if Rune.objects.filter(runeId=participant['stats']['perk3']).count() != 0:
                                        new_player.perk3 = Rune.objects.get(runeId=participant['stats']['perk3'])
                                    else:
                                        check_runes(patch)
                                        new_player.perk3 = Rune.objects.get(runeId=participant['stats']['perk3'])

                                if 'perk4' in participant['stats']:
                                    if Rune.objects.filter(runeId=participant['stats']['perk4']).count() != 0:
                                        new_player.perk4 = Rune.objects.get(runeId=participant['stats']['perk4'])
                                    else:
                                        check_runes(patch)
                                        new_player.perk4 = Rune.objects.get(runeId=participant['stats']['perk4'])

                                if 'perk5' in participant['stats']:
                                    if Rune.objects.filter(runeId=participant['stats']['perk5']).count() != 0:
                                        new_player.perk5 = Rune.objects.get(runeId=participant['stats']['perk5'])
                                    else:
                                        check_runes(patch)
                                        new_player.perk5 = Rune.objects.get(runeId=participant['stats']['perk5'])

                                new_player.save()

                            except Exception as e:
                                with configure_scope() as scope:
                                    scope.set_extra('Match Info JSON', match_info)
                                    capture_exception(e)

    print(Fore.YELLOW + 'Match Created: ' + Style.RESET_ALL + str(game_id))
    return {'isError': False, 'errorMessage': None, 'ignore': False}
