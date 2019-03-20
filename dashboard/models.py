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

class Match(models.Model):
    # IDs
    platformId = models.CharField(max_length=255, blank=False) # Server
    gameId = models.IntegerField(blank=False)
    queueId = models.IntegerField(blank=False)
    seasonId = models.IntegerField(blank=False)
    mapId = models.IntegerField(blank=False)

    # Match Information
    gameMode = models.CharField(max_length=255, blank=False)
    gameType = models.CharField(max_length=255, blank=False)
    gameVersion = models.CharField(max_length=255, blank=False)
    gameDuration = models.IntegerField(blank=False)
    timestamp = models.IntegerField(blank=False)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return str(self.gameId)

    class Meta:
        verbose_name_plural = "Matches"

class Match_Team(models.Model):
    # IDs
    match = models.ForeignKey(Match, related_name='match_team', on_delete=models.CASCADE, null=True, blank=True)

    # General
    win = models.BooleanField(default=False) # 'Fail' = False, 'Win' = True
    teamId = models.IntegerField(blank=False) # 100 = Team1, 200 = Team2

    # Summoners Rift
    firstDragon = models.BooleanField(default=False)
    firstInhibitor = models.BooleanField(default=False)
    firstRiftHerald = models.BooleanField(default=False)
    firstBaron = models.BooleanField(default=False)
    baronKills = models.IntegerField(blank=False)
    riftHeraldKills = models.IntegerField(blank=False)
    firstBlood = models.BooleanField(default=False)
    firstTower = models.BooleanField(default=False)
    inhibitorKills = models.IntegerField(blank=False)
    towerKills = models.IntegerField(blank=False)
    dragonKills = models.IntegerField(blank=False)

    # Other
    dominionVictoryScore = models.IntegerField(blank=False)
    vilemawKills = models.IntegerField(blank=False)

    def __str__(self):
        team = 'Blue' if self.teamId == 100 else 'Red'
        return str(self.match) + ' - Team: ' + team

class Match_Player(models.Model):

    # Participant Identity
    match = models.ForeignKey(Match, related_name='match_players', on_delete=models.CASCADE, blank=False)
    currentPlatformId = models.CharField(max_length=255, blank=False)
    platformId = models.CharField(max_length=255, blank=False)
    matchHistoryUri = models.CharField(max_length=255, blank=False)
    participantId = models.IntegerField(blank=False)
    summonerName = models.CharField(max_length=255, blank=False)

    teamId = models.IntegerField(blank=False) # 100 = Team1, 200 = Team2

    # Participant Stats
    championId = models.IntegerField(blank=False)
    spell1Id = models.IntegerField(blank=False)
    spell2Id = models.IntegerField(blank=False)
    neutralMinionsKilledTeamJungle = models.IntegerField(blank=False)
    visionScore = models.IntegerField(blank=False)
    magicDamageDealtToChampions = models.IntegerField(blank=False)
    largestMultiKill = models.IntegerField(blank=False)
    totalTimeCrowdControlDealt = models.IntegerField(blank=False)
    longestTimeSpentLiving = models.IntegerField(blank=False)
    perk1Var1 = models.IntegerField(blank=False)
    perk1Var3 = models.IntegerField(blank=False)
    perk1Var2 = models.IntegerField(blank=False)
    tripleKills = models.IntegerField(blank=False)
    perk5 = models.IntegerField(blank=False)
    perk4 = models.IntegerField(blank=False)
    playerScore9 = models.IntegerField(blank=False)
    playerScore8 = models.IntegerField(blank=False)
    kills = models.IntegerField(blank=False)
    playerScore1 = models.IntegerField(blank=False)
    playerScore0 = models.IntegerField(blank=False)
    playerScore3 = models.IntegerField(blank=False)
    playerScore2 = models.IntegerField(blank=False)
    playerScore5 = models.IntegerField(blank=False)
    playerScore4 = models.IntegerField(blank=False)
    playerScore7 = models.IntegerField(blank=False)
    playerScore6 = models.IntegerField(blank=False)
    perk5Var1 = models.IntegerField(blank=False)
    perk5Var3 = models.IntegerField(blank=False)
    perk5Var2 = models.IntegerField(blank=False)
    totalScoreRank = models.IntegerField(blank=False)
    neutralMinionsKilled = models.IntegerField(blank=False)
    statPerk1 = models.IntegerField(blank=False)
    statPerk0 = models.IntegerField(blank=False)
    damageDealtToTurrets = models.IntegerField(blank=False)
    physicalDamageDealtToChampions = models.IntegerField(blank=False)
    damageDealtToObjectives = models.IntegerField(blank=False)
    perk2Var2 = models.IntegerField(blank=False)
    perk2Var3 = models.IntegerField(blank=False)
    totalUnitsHealed = models.IntegerField(blank=False)
    perk2Var1 = models.IntegerField(blank=False)
    perk4Var1 = models.IntegerField(blank=False)
    totalDamageTaken = models.IntegerField(blank=False)
    perk4Var3 = models.IntegerField(blank=False)
    wardsKilled = models.IntegerField(blank=False)
    largestCriticalStrike = models.IntegerField(blank=False)
    largestKillingSpree = models.IntegerField(blank=False)
    quadraKills = models.IntegerField(blank=False)
    magicDamageDealt = models.IntegerField(blank=False)
    firstBloodAssist = models.BooleanField(default=False)
    item2 = models.IntegerField(blank=False)
    item3 = models.IntegerField(blank=False)
    item0 = models.IntegerField(blank=False)
    item1 = models.IntegerField(blank=False)
    item6 = models.IntegerField(blank=False)
    item4 = models.IntegerField(blank=False)
    item5 = models.IntegerField(blank=False)
    perk1 = models.IntegerField(blank=False)
    perk0 = models.IntegerField(blank=False)
    perk3 = models.IntegerField(blank=False)
    perk2 = models.IntegerField(blank=False)
    perk3Var3 = models.IntegerField(blank=False)
    perk3Var2 = models.IntegerField(blank=False)
    perk3Var1 = models.IntegerField(blank=False)
    damageSelfMitigated = models.IntegerField(blank=False)
    magicalDamageTaken = models.IntegerField(blank=False)
    perk0Var2 = models.IntegerField(blank=False)
    firstInhibitorKill = models.BooleanField(default=False)
    trueDamageTaken = models.IntegerField(blank=False)
    assists = models.IntegerField(blank=False)
    perk4Var2 = models.IntegerField(blank=False)
    goldSpent = models.IntegerField(blank=False)
    trueDamageDealt = models.IntegerField(blank=False)
    participantId = models.IntegerField(blank=False)
    physicalDamageDealt = models.IntegerField(blank=False)
    sightWardsBoughtInGame = models.IntegerField(blank=False)
    totalDamageDealtToChampions = models.IntegerField(blank=False)
    physicalDamageTaken = models.IntegerField(blank=False)
    totalPlayerScore = models.IntegerField(blank=False)
    win = models.BooleanField(default=False)
    objectivePlayerScore = models.IntegerField(blank=False)
    totalDamageDealt = models.IntegerField(blank=False)
    neutralMinionsKilledEnemyJungle = models.IntegerField(blank=False)
    deaths = models.IntegerField(blank=False)
    wardsPlaced = models.IntegerField(blank=False)
    perkPrimaryStyle = models.IntegerField(blank=False)
    perkSubStyle = models.IntegerField(blank=False)
    turretKills = models.IntegerField(blank=False)
    firstBloodKill = models.BooleanField(default=False)
    trueDamageDealtToChampions = models.IntegerField(blank=False)
    goldEarned = models.IntegerField(blank=False)
    killingSprees = models.IntegerField(blank=False)
    unrealKills = models.IntegerField(blank=False)
    firstTowerAssist = models.BooleanField(default=False)
    firstTowerKill = models.BooleanField(default=False)
    champLevel = models.IntegerField(blank=False)
    doubleKills = models.IntegerField(blank=False)
    inhibitorKills = models.IntegerField(blank=False)
    firstInhibitorAssist = models.BooleanField(default=False)
    perk0Var1 = models.IntegerField(blank=False)
    combatPlayerScore = models.IntegerField(blank=False)
    perk0Var3 = models.IntegerField(blank=False)
    visionWardsBoughtInGame = models.IntegerField(blank=False)
    pentaKills = models.IntegerField(blank=False)
    totalHeal = models.IntegerField(blank=False)
    totalMinionsKilled = models.IntegerField(blank=False)
    timeCCingOthers = models.IntegerField(blank=False)
    statPerk2 = models.IntegerField(blank=False)

    def __str__(self):
        return str(self.match) + ' - Player: ' + str(self.summonerName)
