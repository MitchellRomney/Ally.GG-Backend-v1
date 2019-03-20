from django.contrib.auth.models import User
from dashboard.models import Summoner, Match, Match_Team, Match_Player
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class SummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        fields = (
            # IDs
            'summonerName',
            'summonerId',
            'puuid',
            'accountId',

            # General
            'server',
            'profileIconId',
            'summonerLevel',
            'user',

            # SoloQ
            'soloQ_leagueId',
            'soloQ_leagueName',
            'soloQ_tier',
            'soloQ_hotStreak',
            'soloQ_wins',
            'soloQ_losses',
            'soloQ_veteran',
            'soloQ_rank',
            'soloQ_inactive',
            'soloQ_freshBlood',
            'soloQ_leaguePoints',

            # System
            'date_created',
            'date_updated'
            )

class MatchPlayerSerializer(serializers.ModelSerializer):

    gameId = serializers.ReadOnlyField(source='match.gameId')

    class Meta:
        model = Match_Player
        fields = (
            # Key IDs & Participant Identity
            'match',
            'gameId',
            'currentPlatformId',
            'platformId',
            'matchHistoryUri',
            'participantId',
            'summonerName',

            'teamId',

            # General Player Information
            'spell1Id',
            'spell2Id',
            'championId',

            # Stats
                ## Minions
                'totalMinionsKilled',
                'neutralMinionsKilled',
                'neutralMinionsKilledTeamJungle',
                'neutralMinionsKilledEnemyJungle',

                ## Vision
                'visionScore',
                'sightWardsBoughtInGame',
                'visionWardsBoughtInGame',
                'wardsKilled',
                'wardsPlaced',

                ## Damage Dealt
                'totalDamageDealt',
                'totalDamageDealtToChampions',
                'physicalDamageDealt',
                'physicalDamageDealtToChampions',
                'magicDamageDealt',
                'magicDamageDealtToChampions',
                'trueDamageDealt',
                'trueDamageDealtToChampions',
                'largestCriticalStrike',

                ## Damage Taken
                'totalDamageTaken',
                'physicalDamageTaken',
                'magicalDamageTaken',
                'trueDamageTaken',
                'damageSelfMitigated',

                # Objectives
                'turretKills',
                'inhibitorKills',
                'damageDealtToTurrets',
                'damageDealtToObjectives',
                'firstInhibitorKill',
                'firstInhibitorAssist',
                'firstTowerAssist',
                'firstTowerKill',

                ## Kills
                'kills',
                'assists',
                'killingSprees',
                'unrealKills',
                'doubleKills',
                'tripleKills',
                'quadraKills',
                'pentaKills',
                'largestMultiKill',
                'largestKillingSpree',
                'firstBloodKill',
                'firstBloodAssist',

                # Crowd Control
                'timeCCingOthers',
                'totalTimeCrowdControlDealt',

                # Health
                'totalUnitsHealed',
                'totalHeal',
                'deaths',

                # Perks
                'perk0',
                'perk1',
                'perk2',
                'perk3',
                'perk4',
                'perk5',
                'statPerk0',
                'statPerk1',
                'statPerk1',
                'perk0Var1',
                'perk0Var2',
                'perk0Var3',
                'perk1Var1',
                'perk1Var2',
                'perk1Var3',
                'perk2Var1',
                'perk2Var2',
                'perk2Var3',
                'perk3Var1',
                'perk3Var2',
                'perk3Var3',
                'perk4Var1',
                'perk4Var2',
                'perk4Var3',
                'perk5Var1',
                'perk5Var2',
                'perk5Var3',
                'perkPrimaryStyle',
                'perkSubStyle',

                # Player Score
                'playerScore0',
                'playerScore1',
                'playerScore2',
                'playerScore3',
                'playerScore4',
                'playerScore5',
                'playerScore6',
                'playerScore7',
                'playerScore8',
                'playerScore9',
                'objectivePlayerScore',
                'combatPlayerScore',
                'totalPlayerScore',
                'totalScoreRank',

                # Items
                'item0',
                'item1',
                'item2',
                'item3',
                'item4',
                'item5',
                'item6',

                # Other
                'longestTimeSpentLiving',
                'goldEarned',
                'goldSpent',
                'win',
                'champLevel',
        )

class MatchTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match_Team
        fields = (
            'match',

            # General
            'win',
            'teamId',

            # Summoners Rift
            'firstDragon',
            'firstInhibitor',
            'firstRiftHerald',
            'firstBaron',
            'baronKills',
            'riftHeraldKills',
            'firstBlood',
            'firstTower',
            'inhibitorKills',
            'towerKills',
            'dragonKills',

            # Other
            'dominionVictoryScore',
            'vilemawKills',
        )

class MatchSerializer(serializers.ModelSerializer):
    match_team = MatchTeamSerializer(many=True, read_only=True)
    match_players = MatchPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Match
        fields = (
            'platformId',
            'gameId',
            'queueId',
            'seasonId',
            'mapId',
            'gameMode',
            'gameType',
            'gameVersion',
            'gameDuration',
            'timestamp',
            'date_created',
            'match_team',
            'match_players',
        )
