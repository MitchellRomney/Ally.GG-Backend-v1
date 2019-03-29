from django.contrib.auth.models import User
from dashboard.models import *
from rest_framework import serializers
from datetime import datetime
from django.utils import timezone
import time, timeago

class MatchSummonerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        fields = ('summonerName',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class ChampionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Champion
        fields = (
            'version',
            'champId',
            'name',
            'key',
            'title',
            'blurb',
            'info_attack',
            'info_defense',
            'info_magic',
            'info_difficulty',

            # Images
            'image_full',
            'image_sprite',
            'image_group',
            'image_x',
            'image_y',
            'image_w',
            'image_h',

            # Stats & Info
            'tags',
            'partype',
            'stats_hp',
            'stats_hpperlevel',
            'stats_mp',
            'stats_mpperlevel',
            'stats_movespeed',
            'stats_armor',
            'stats_armorperlevel',
            'stats_spellblock',
            'stats_spellblockperlevel',
            'stats_attackrange',
            'stats_hpregen',
            'stats_hpregenperlevel',
            'stats_mpregen',
            'stats_mpregenperlevel',
            'stats_crit',
            'stats_critperlevel',
            'stats_attackdamage',
            'stats_attackdamageperlevel',
            'stats_attackspeedperlevel',
            'stats_attackspeed',
        )

class MatchPlayerSerializer(serializers.ModelSerializer):

    gameId = serializers.ReadOnlyField(source='match.gameId')
    summoner = MatchSummonerSerializer()
    champion = ChampionSerializer()

    class Meta:
        model = Player
        fields = (
            # Key IDs & Participant Identity
            'match',
            'gameId',
            'currentPlatformId',
            'platformId',
            'matchHistoryUri',
            'participantId',
            'summoner',

            'team',

            # General Player Information
            'spell1Id',
            'spell2Id',
            'champion',

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
        model = Team
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

class MatchListSerializer(serializers.ModelSerializer):
    # def get_timestamp(self, obj):
    #     return timeago.format(datetime.fromtimestamp(obj.timestamp/1000.), datetime.now())

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
        )

class MatchSerializer(serializers.ModelSerializer):
    queue = serializers.CharField(source='get_queueId_display')
    season = serializers.CharField(source='get_seasonId_display')
    map = serializers.CharField(source='get_mapId_display')
    Team = MatchTeamSerializer(many=True, read_only=True)
    Players = MatchPlayerSerializer(many=True, read_only=True)

    timestamp = serializers.SerializerMethodField()

    def get_timestamp(self, obj):
        return timeago.format(obj.timestamp, timezone.now())

    class Meta:
        model = Match
        fields = (
            'platformId',
            'gameId',
            'queue',
            'season',
            'map',
            'gameMode',
            'gameType',
            'gameVersion',
            'gameDuration',
            'timestamp',
            'date_created',
            'Team',
            'Players',
        )

class SummonerSerializer(serializers.ModelSerializer):
    Matches = MatchListSerializer(many=True, read_only=True)

    class Meta:
        model = Summoner
        fields = (
            # IDs
            'user_profile',
            'summonerName',
            'summonerId',
            'puuid',
            'accountId',

            # General
            'server',
            'profileIconId',
            'summonerLevel',

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

            # Matches
            'Matches',

            # System
            'date_created',
            'date_updated',
            )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["Matches"] = sorted(response["Matches"], key=lambda x: x["timestamp"])
        return response
