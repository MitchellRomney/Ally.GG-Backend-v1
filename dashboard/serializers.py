from django.contrib.auth.models import User
from dashboard.models import Summoner
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

class SummonerSerializer(serializers.HyperlinkedModelSerializer):
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
