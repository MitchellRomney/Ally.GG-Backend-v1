from dashboard.functions.game_data import *
from sentry_sdk import configure_scope, capture_exception
from datetime import datetime
import re
import pytz


def fetch_match_list(summoner_id, server='OC1'):
    # Get the Summoner that you're fetching for.
    summoner = Summoner.objects.get(summonerId=summoner_id)

    # Get the match list from the Riot API.
    matches = fetch_riot_api(server, 'match', 'v4', 'matchlists/by-account/' + summoner.accountId, '?endIndex=10')

    # Make sure that the matches actually exist in the response.
    if 'matches' in matches:
        # Return the list of matches.
        return matches['matches']


def create_match(game_id, server='OC1'):
    # Count variables to check integrity at the end.
    team_count = 0
    player_count = 0

    # Fetch the match information from the Riot API.
    match_data = fetch_riot_api(server, 'match', 'v4', 'matches/' + str(game_id))

    # Convert the timestamp into a valid DateTime.
    timestamp = datetime.utcfromtimestamp(match_data['gameCreation'] / 1000.).replace(tzinfo=pytz.UTC)

    # Do not add matches that were before 2018 Pre-Season or that are tutorial games.
    if match_data['seasonId'] >= 10 and match_data['queueId'] < 2000:
        new_match = Match(
            gameId=match_data['gameId'],
            platformId=match_data['platformId'],
            queueId=match_data['queueId'],
            seasonId=match_data['seasonId'],
            mapId=match_data['mapId'],

            gameMode=match_data['gameMode'],
            gameType=match_data['gameType'],
            gameVersion=match_data['gameVersion'],
            gameDuration=match_data['gameDuration'],
            timestamp=timestamp,
        )
    else:
        return {'isError': False, 'errorMessage': None, 'ignore': True}

    # Double check that the match doesn't already exist.
    if Match.objects.filter(gameId=match_data['gameId']).count() == 0:
        try:
            new_match.save()
        except IntegrityError:  # Even though we triple checked, some matches still double up.
            return {'isError': False, 'errorMessage': None, 'ignore': True}
    else:
        return {'isError': False, 'errorMessage': None, 'ignore': True}

    # Iterate through the teams, create according Team objects.
    for team_data in match_data['teams']:
        # Add to the team count.
        team_count += 1

        # Check that the team doesn't somehow exist already, then create team.
        if Team.objects.filter(match=new_match, teamId=team_data['teamId']).count() == 0:
            try:
                create_team(new_match, team_data)
            except KeyError as key_error:
                new_match.delete()
                capture_exception(key_error)
                return {'isError': True, 'errorMessage': '{0}'.format(key_error), 'ignore': True}
            except TypeError as type_error:
                new_match.delete()
                capture_exception(type_error)
                return {'isError': True, 'errorMessage': '{0}'.format(type_error), 'ignore': True}
            except IntegrityError:
                return {'isError': False, 'errorMessage': None, 'ignore': True}
        else:
            return {'isError': False, 'errorMessage': None, 'ignore': True}

    # Iterate through the players, create according Player objects.
    for player_account_info in match_data['participantIdentities']:
        blue_team = Team.objects.get(match=new_match, teamId=100)
        red_team = Team.objects.get(match=new_match, teamId=200)
        player_team = blue_team if player_account_info['participantId'] <= 5 else red_team

        for player_data in match_data['participants']:
            if player_data['participantId'] == player_account_info['participantId']:
                # Add to the player count.
                player_count += 1

                # Check if the player is a bot.
                if player_account_info['player']['accountId'] != '0':

                    # Add Summoner to database if it doesn't already exist.
                    if Summoner.objects.filter(summonerId=player_account_info['player']['summonerId']).count() == 0:
                        add_summoner('SummonerId', player_account_info['player']['summonerId'], server)

                    # Add Summoner to Match.summoners relation field.
                    new_match.summoners.add(
                        Summoner.objects.get(summonerId=player_account_info['player']['summonerId']))

                # Create the Player.
                try:
                    new_player = create_player(new_match, player_team, player_account_info, player_data)
                except KeyError as key_error:
                    new_match.delete()
                    capture_exception(key_error)
                    return {'isError': True, 'errorMessage': '{0}'.format(key_error), 'ignore': True}
                except TypeError as type_error:
                    new_match.delete()
                    capture_exception(type_error)
                    return {'isError': True, 'errorMessage': '{0}'.format(type_error), 'ignore': True}
                except IntegrityError:
                    return {'isError': False, 'errorMessage': None, 'ignore': True}

                # Add Summoner to players Many to Many relation field on Match.
                new_match.players.add(new_player)

    # Integrity check, need to make sure that the Match has the right number of Teams and Players.
    if Team.objects.filter(match=new_match).count() != team_count:
        with configure_scope() as scope:
            scope.set_extra("Expected Team Count", team_count)
            scope.set_extra("Real Team Count", Team.objects.filter(match=new_match).count())
            scope.set_extra("Match Data", match_data)
        print(
            Fore.RED + '[ERROR]: '
            + Style.RESET_ALL + 'Team count is off (Got '
            + str(Team.objects.filter(match=new_match).count())
            + ', expected ' + str(team_count) + ') - deleting Match.'
        )
        new_match.delete()
        return {'isError': True, 'errorMessage': 'Error creating Match Teams.', 'ignore': False}

    elif Player.objects.filter(match=new_match).count() != player_count:
        with configure_scope() as scope:
            scope.set_extra("Expected Player Count", player_count)
            scope.set_extra("Real Player Count", Player.objects.filter(match=new_match).count())
            scope.set_extra("Match Data", match_data)
        print(
            Fore.RED + '[ERROR]: '
            + Style.RESET_ALL + 'Player count is off (Got '
            + str(Player.objects.filter(match=new_match).count())
            + ', expected ' + str(player_count) + ') - deleting Match.'
        )
        new_match.delete()
        return {'isError': True, 'errorMessage': 'Error creating Match Players.', 'ignore': False}

    return {'isError': False, 'errorMessage': None, 'ignore': False, 'match': new_match}


def create_team(match, team_data):
    # Convert the 'win' field to a valid boolean based on result.
    if 'win' in team_data:
        result = False if team_data['win'] == 'Fail' else True
    else:  # Win field doesn't exist on the bot team in Odyssey game mode.
        result = False

    # Build the team object.
    new_team = Team(
        # General
        match=match,
        win=result,
        teamId=team_data['teamId'],

        # Summoners Rift
        firstDragon=team_data['firstDragon'],
        firstInhibitor=team_data['firstInhibitor'],
        firstRiftHerald=team_data['firstRiftHerald'],
        firstBaron=team_data['firstBaron'],
        baronKills=team_data['baronKills'],
        riftHeraldKills=team_data['riftHeraldKills'],
        firstBlood=team_data['firstBlood'],
        firstTower=team_data['firstTower'],
        inhibitorKills=team_data['inhibitorKills'],
        towerKills=team_data['towerKills'],
        dragonKills=team_data['dragonKills'],

        # Other
        dominionVictoryScore=team_data['dominionVictoryScore'],
        vilemawKills=team_data['vilemawKills'],
    )

    # Final check to make sure the team doesn't already exist.
    if Team.objects.filter(match=match, teamId=team_data['teamId']).count() == 0:
        new_team.save()

        return new_team


def create_player(match, player_team, player_account_info, player_data):
    # Build the Player object.
    new_player = Player(
        # Key IDs & Participant Identity
        match=Match.objects.get(gameId=match.gameId),
        currentPlatformId=player_account_info['player']['currentPlatformId'],
        platformId=player_account_info['player']['platformId'],
        matchHistoryUri=player_account_info['player']['matchHistoryUri'],
        participantId=player_account_info['participantId'],

        team=player_team,

        # General Player Information
        spell1Id=SummonerSpell.objects.get(key=player_data['spell1Id']),
        spell2Id=SummonerSpell.objects.get(key=player_data['spell2Id']),
        champion=Champion.objects.get(key=player_data['championId']),

        # Minions
        totalMinionsKilled=player_data['stats']['totalMinionsKilled'],
        neutralMinionsKilled=player_data['stats']['neutralMinionsKilled'],
        neutralMinionsKilledTeamJungle=player_data['stats'][
            'neutralMinionsKilledTeamJungle'] if 'neutralMinionsKilledTeamJungle' in player_data['stats'] else 0,
        neutralMinionsKilledEnemyJungle=player_data['stats'][
            'neutralMinionsKilledEnemyJungle'] if 'neutralMinionsKilledEnemyJungle' in player_data['stats'] else 0,

        # Vision
        visionScore=player_data['stats']['visionScore'],
        sightWardsBoughtInGame=player_data['stats']['sightWardsBoughtInGame'],
        visionWardsBoughtInGame=player_data['stats']['visionWardsBoughtInGame'],
        wardsKilled=player_data['stats']['wardsKilled'] if 'wardsKilled' in player_data['stats'] else 0,
        wardsPlaced=player_data['stats']['wardsPlaced'] if 'wardsKilled' in player_data['stats'] else 0,

        # Damage Dealt
        totalDamageDealt=player_data['stats']['totalDamageDealt'],
        totalDamageDealtToChampions=player_data['stats']['totalDamageDealtToChampions'],
        physicalDamageDealt=player_data['stats']['physicalDamageDealt'],
        physicalDamageDealtToChampions=player_data['stats']['physicalDamageDealtToChampions'],
        magicDamageDealt=player_data['stats']['magicDamageDealt'],
        magicDamageDealtToChampions=player_data['stats']['magicDamageDealtToChampions'],
        trueDamageDealt=player_data['stats']['trueDamageDealt'],
        trueDamageDealtToChampions=player_data['stats']['trueDamageDealtToChampions'],
        largestCriticalStrike=player_data['stats']['largestCriticalStrike'],

        # Damage Taken
        totalDamageTaken=player_data['stats']['totalDamageTaken'],
        physicalDamageTaken=player_data['stats']['physicalDamageTaken'],
        magicalDamageTaken=player_data['stats']['magicalDamageTaken'],
        trueDamageTaken=player_data['stats']['trueDamageTaken'],
        damageSelfMitigated=player_data['stats']['damageSelfMitigated'],

        # Objectives
        turretKills=player_data['stats']['turretKills'],
        inhibitorKills=player_data['stats']['inhibitorKills'],
        damageDealtToTurrets=player_data['stats']['damageDealtToTurrets'],
        damageDealtToObjectives=player_data['stats']['damageDealtToObjectives'],
        firstInhibitorKill=player_data['stats']['firstInhibitorKill'] if 'firstInhibitorKill' in player_data[
            'stats'] else False,
        firstInhibitorAssist=player_data['stats']['firstInhibitorAssist'] if 'firstInhibitorAssist' in player_data[
            'stats'] else False,
        firstTowerAssist=player_data['stats']['firstTowerAssist'] if 'firstTowerAssist' in player_data[
            'stats'] else False,
        firstTowerKill=player_data['stats']['firstTowerKill'] if 'firstTowerKill' in player_data['stats'] else False,

        # Kills
        kills=player_data['stats']['kills'],
        assists=player_data['stats']['assists'],
        killingSprees=player_data['stats']['killingSprees'],
        unrealKills=player_data['stats']['unrealKills'],
        doubleKills=player_data['stats']['doubleKills'],
        tripleKills=player_data['stats']['tripleKills'],
        quadraKills=player_data['stats']['quadraKills'],
        pentaKills=player_data['stats']['pentaKills'],
        largestMultiKill=player_data['stats']['largestMultiKill'],
        largestKillingSpree=player_data['stats']['largestKillingSpree'],
        firstBloodKill=player_data['stats']['firstBloodKill'] if 'firstBloodKill' in player_data['stats'] else False,
        firstBloodAssist=player_data['stats']['firstBloodAssist'] if 'firstBloodAssist' in player_data[
            'stats'] else False,

        # Crowd Control
        timeCCingOthers=player_data['stats']['timeCCingOthers'],
        totalTimeCrowdControlDealt=player_data['stats']['totalTimeCrowdControlDealt'],

        # Health
        totalUnitsHealed=player_data['stats']['totalUnitsHealed'],
        totalHeal=player_data['stats']['totalHeal'],
        deaths=player_data['stats']['deaths'],

        # Perks
        statPerk0=player_data['stats']['statPerk0'] if 'statPerk0' in player_data['stats'] else 0,
        statPerk1=player_data['stats']['statPerk1'] if 'statPerk0' in player_data['stats'] else 0,
        statPerk2=player_data['stats']['statPerk1'] if 'statPerk0' in player_data['stats'] else 0,
        perk0Var1=player_data['stats']['perk0Var1'] if 'perk0Var1' in player_data['stats'] else 0,
        perk0Var2=player_data['stats']['perk0Var2'] if 'perk0Var2' in player_data['stats'] else 0,
        perk0Var3=player_data['stats']['perk0Var3'] if 'perk0Var3' in player_data['stats'] else 0,
        perk1Var1=player_data['stats']['perk1Var1'] if 'perk1Var1' in player_data['stats'] else 0,
        perk1Var2=player_data['stats']['perk1Var2'] if 'perk1Var2' in player_data['stats'] else 0,
        perk1Var3=player_data['stats']['perk1Var3'] if 'perk1Var3' in player_data['stats'] else 0,
        perk2Var1=player_data['stats']['perk2Var1'] if 'perk2Var1' in player_data['stats'] else 0,
        perk2Var2=player_data['stats']['perk2Var2'] if 'perk2Var2' in player_data['stats'] else 0,
        perk2Var3=player_data['stats']['perk2Var3'] if 'perk2Var3' in player_data['stats'] else 0,
        perk3Var1=player_data['stats']['perk3Var1'] if 'perk3Var1' in player_data['stats'] else 0,
        perk3Var2=player_data['stats']['perk3Var2'] if 'perk3Var2' in player_data['stats'] else 0,
        perk3Var3=player_data['stats']['perk3Var3'] if 'perk3Var3' in player_data['stats'] else 0,
        perk4Var1=player_data['stats']['perk4Var1'] if 'perk4Var1' in player_data['stats'] else 0,
        perk4Var2=player_data['stats']['perk4Var2'] if 'perk4Var2' in player_data['stats'] else 0,
        perk4Var3=player_data['stats']['perk4Var3'] if 'perk4Var3' in player_data['stats'] else 0,
        perk5Var1=player_data['stats']['perk5Var1'] if 'perk5Var1' in player_data['stats'] else 0,
        perk5Var2=player_data['stats']['perk5Var2'] if 'perk5Var2' in player_data['stats'] else 0,
        perk5Var3=player_data['stats']['perk5Var3'] if 'perk5Var3' in player_data['stats'] else 0,
        perkPrimaryStyle=player_data['stats']['perkPrimaryStyle'] if 'perkPrimaryStyle' in player_data['stats'] else 0,
        perkSubStyle=player_data['stats']['perkSubStyle'] if 'perkSubStyle' in player_data['stats'] else 0,

        # Player Score
        playerScore0=player_data['stats']['playerScore0'],
        playerScore1=player_data['stats']['playerScore1'],
        playerScore2=player_data['stats']['playerScore2'],
        playerScore3=player_data['stats']['playerScore3'],
        playerScore4=player_data['stats']['playerScore4'],
        playerScore5=player_data['stats']['playerScore5'],
        playerScore6=player_data['stats']['playerScore6'],
        playerScore7=player_data['stats']['playerScore7'],
        playerScore8=player_data['stats']['playerScore8'],
        playerScore9=player_data['stats']['playerScore9'],
        objectivePlayerScore=player_data['stats']['objectivePlayerScore'],
        combatPlayerScore=player_data['stats']['combatPlayerScore'],
        totalPlayerScore=player_data['stats']['totalPlayerScore'],
        totalScoreRank=player_data['stats']['totalScoreRank'],

        # Other
        longestTimeSpentLiving=player_data['stats']['longestTimeSpentLiving'],
        goldEarned=player_data['stats']['goldEarned'],
        goldSpent=player_data['stats']['goldSpent'],
        win=player_data['stats']['win'],
        champLevel=player_data['stats']['champLevel'],
    )

    # Set the lane that the player spent the start of the game in.
    new_player.lane = player_data['timeline']['lane']

    # Add relation to Summoner object if the Player isn't a bot.
    if 'summonerId' in player_account_info['player']:
        new_player.summoner = Summoner.objects.get(summonerId=player_account_info['player']['summonerId'])

    # Get the patch version from the game to fetch missing items & runes.
    patch = re.compile('\d\.\d{1,2}\.').findall(match.gameVersion)[0] + '1'

    # Check if all items exist in database.
    if Item.objects.filter(itemId=player_data['stats']['item0']).count() == 0 \
            or Item.objects.filter(itemId=player_data['stats']['item1']).count() == 0 \
            or Item.objects.filter(itemId=player_data['stats']['item2']).count() == 0 \
            or Item.objects.filter(itemId=player_data['stats']['item3']).count() == 0 \
            or Item.objects.filter(itemId=player_data['stats']['item4']).count() == 0 \
            or Item.objects.filter(itemId=player_data['stats']['item5']).count() == 0 \
            or Item.objects.filter(itemId=player_data['stats']['item6']).count() == 0:
        check_items(patch)

    # Add all items to the player object.
    new_player.item0 = Item.objects.get(itemId=player_data['stats']['item0'])
    new_player.item1 = Item.objects.get(itemId=player_data['stats']['item1'])
    new_player.item2 = Item.objects.get(itemId=player_data['stats']['item2'])
    new_player.item3 = Item.objects.get(itemId=player_data['stats']['item3'])
    new_player.item4 = Item.objects.get(itemId=player_data['stats']['item4'])
    new_player.item5 = Item.objects.get(itemId=player_data['stats']['item5'])
    new_player.item6 = Item.objects.get(itemId=player_data['stats']['item6'])

    # Check all Runes if they exist in the data, and if they exist in the database. Then add to Player.
    if 'perk0' in player_data['stats']:
        if Rune.objects.filter(runeId=player_data['stats']['perk0']).count() == 0:
            check_runes(patch)
        new_player.perk0 = Rune.objects.get(runeId=player_data['stats']['perk0'])

    if 'perk1' in player_data['stats']:
        if Rune.objects.filter(runeId=player_data['stats']['perk1']).count() == 0:
            check_runes(patch)
        new_player.perk1 = Rune.objects.get(runeId=player_data['stats']['perk1'])

    if 'perk2' in player_data['stats']:
        if Rune.objects.filter(runeId=player_data['stats']['perk2']).count() == 0:
            check_runes(patch)
        new_player.perk2 = Rune.objects.get(runeId=player_data['stats']['perk2'])

    if 'perk3' in player_data['stats']:
        if Rune.objects.filter(runeId=player_data['stats']['perk3']).count() == 0:
            check_runes(patch)
        new_player.perk3 = Rune.objects.get(runeId=player_data['stats']['perk3'])

    if 'perk4' in player_data['stats']:
        if Rune.objects.filter(runeId=player_data['stats']['perk4']).count() == 0:
            check_runes(patch)
        new_player.perk4 = Rune.objects.get(runeId=player_data['stats']['perk4'])

    if 'perk5' in player_data['stats']:
        if Rune.objects.filter(runeId=player_data['stats']['perk5']).count() == 0:
            check_runes(patch)
        new_player.perk5 = Rune.objects.get(runeId=player_data['stats']['perk5'])

    # Double check the Match still exists in database.
    if Match.objects.filter(gameId=match.gameId).count() != 0:
        # Double check that the Player doesn't exist already in database.
        if Player.objects.filter(match=match, participantId=player_account_info['participantId']).count() == 0:
            # Insert Player into database.
            new_player.save()

            return new_player
