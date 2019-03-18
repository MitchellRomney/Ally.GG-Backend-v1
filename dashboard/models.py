from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Summoner(models.Model):
    # IDs
    summonerName = models.CharField(max_length=255, blank=False)
    summonerId = models.CharField(max_length=255, unique=True, blank=False) # Same as Id in some cases.
    puuid = models.CharField(max_length=255, unique=True, blank=False)
    accountId = models.CharField(max_length=255, unique=True, blank=False)

    # General
    server = models.CharField(max_length=255, blank=False)
    profileIconId = models.IntegerField(blank=True, default=1)
    summonerLevel = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    # SoloQ
    soloQ_leagueId = models.CharField(max_length=255, blank=True)
    soloQ_leagueName = models.CharField(max_length=255, blank=True)
    soloQ_tier = models.CharField(max_length=255, blank=True)
    soloQ_hotStreak = models.BooleanField(default=False)
    soloQ_wins = models.IntegerField(null=True, blank=True, default=0)
    soloQ_losses = models.IntegerField(null=True, blank=True, default=0)
    soloQ_veteran = models.BooleanField(default=False)
    soloQ_rank = models.CharField(max_length=255, null=True, blank=True)
    soloQ_inactive = models.BooleanField(default=False)
    soloQ_freshBlood = models.BooleanField(default=False)
    soloQ_leaguePoints = models.IntegerField(null=True, blank=True, default=0)

    # System
    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_updated = models.DateTimeField(blank=False)

    def __str__(self):
        return self.summonerName
