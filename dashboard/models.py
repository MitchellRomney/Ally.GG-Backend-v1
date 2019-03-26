from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import json

class Profile(models.Model):
    user = models.ForeignKey(User, related_name="Profiles", on_delete=models.CASCADE, blank=False)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=False)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_modified = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.user.username

class Champion(models.Model):
    # General
    version = models.CharField(max_length=255, blank=False) # What version did we gather this data from (should be latest).
    champId = models.CharField(max_length=255, blank=False) # Basically champion name without spaces and extras.
    name = models.CharField(max_length=255, blank=False)
    key = models.CharField(max_length=255, blank=False) # Numerical ID
    title = models.CharField(max_length=255, blank=False)
    blurb = models.TextField(max_length=255, blank=False)
    info_attack = models.BigIntegerField(blank=False)
    info_defense = models.BigIntegerField(blank=False)
    info_magic = models.BigIntegerField(blank=False)
    info_difficulty = models.BigIntegerField(blank=False)

    # Images
    image_full = models.CharField(max_length=255, blank=False)
    image_sprite = models.CharField(max_length=255, blank=False)
    image_group = models.CharField(max_length=255, blank=False)
    image_x = models.BigIntegerField(blank=False, default=0)
    image_y = models.BigIntegerField(blank=False, default=0)
    image_w = models.BigIntegerField(blank=False, default=0)
    image_h = models.BigIntegerField(blank=False, default=0)

    # Stats & Info
    tags = models.CharField(max_length=255, blank=False)
    partype = models.CharField(max_length=255, blank=False)
    stats_hp = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_hpperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_mp = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_mpperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_movespeed = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_armor = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_armorperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_spellblock = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_spellblockperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackrange = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_hpregen = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_hpregenperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_mpregen = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_mpregenperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_crit = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_critperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackdamage = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackdamageperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackspeedperlevel = models.DecimalField(max_digits=8, decimal_places=4, blank=False)
    stats_attackspeed = models.DecimalField(max_digits=8, decimal_places=4, blank=False)

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)

    def __str__(self):
        return self.champId


class Summoner(models.Model):
    # IDs
    user_profile = models.ForeignKey(Profile, related_name="Summoners", on_delete=models.SET_NULL, null=True, blank=True)
    summonerName = models.CharField(max_length=255, blank=False)
    summonerId = models.CharField(max_length=255, primary_key=True, unique=True, blank=False) # Same as Id in some cases.
    puuid = models.CharField(max_length=255, unique=True, blank=False)
    accountId = models.CharField(max_length=255, unique=True, blank=False)

    # General
    server = models.CharField(max_length=255, blank=False)
    profileIconId = models.BigIntegerField(blank=True, default=1)
    summonerLevel = models.CharField(max_length=255, blank=True)

    # SoloQ
    soloQ_leagueId = models.CharField(max_length=255, blank=True)
    soloQ_leagueName = models.CharField(max_length=255, blank=True)
    soloQ_tier = models.CharField(max_length=255, blank=True)
    soloQ_hotStreak = models.BooleanField(default=False)
    soloQ_wins = models.BigIntegerField(null=True, blank=True, default=0)
    soloQ_losses = models.BigIntegerField(null=True, blank=True, default=0)
    soloQ_veteran = models.BooleanField(default=False)
    soloQ_rank = models.CharField(max_length=255, null=True, blank=True)
    soloQ_inactive = models.BooleanField(default=False)
    soloQ_freshBlood = models.BooleanField(default=False)
    soloQ_leaguePoints = models.BigIntegerField(null=True, blank=True, default=0)

    # System
    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_updated = models.DateTimeField(blank=False)

    def __str__(self):
        return self.summonerName

    def __unicode__(self):
        return self.summonerName

class Match(models.Model):
    # IDs
    platformId = models.CharField(max_length=255, blank=False) # Server
    gameId = models.BigIntegerField(blank=False)
    queueId = models.BigIntegerField(blank=False)
    seasonId = models.BigIntegerField(blank=False)
    mapId = models.BigIntegerField(blank=False)

    # Players
    players = models.ManyToManyField('Summoner', related_name='Matches')

    # Match Information
    gameMode = models.CharField(max_length=255, blank=False)
    gameType = models.CharField(max_length=255, blank=False)
    gameVersion = models.CharField(max_length=255, blank=False)
    gameDuration = models.BigIntegerField(blank=False)
    timestamp = models.BigIntegerField(blank=False)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return str(self.gameId)

    class Meta:
        verbose_name_plural = "Matches"

class Team(models.Model):
    # IDs
    match = models.ForeignKey(Match, related_name='Teams', on_delete=models.CASCADE, null=True, blank=True)

    # General
    win = models.BooleanField(default=False) # 'Fail' = False, 'Win' = True
    teamId = models.BigIntegerField(blank=False) # 100 = Team1, 200 = Team2

    # Summoners Rift
    firstDragon = models.BooleanField(default=False)
    firstInhibitor = models.BooleanField(default=False)
    firstRiftHerald = models.BooleanField(default=False)
    firstBaron = models.BooleanField(default=False)
    baronKills = models.BigIntegerField(blank=False)
    riftHeraldKills = models.BigIntegerField(blank=False)
    firstBlood = models.BooleanField(default=False)
    firstTower = models.BooleanField(default=False)
    inhibitorKills = models.BigIntegerField(blank=False)
    towerKills = models.BigIntegerField(blank=False)
    dragonKills = models.BigIntegerField(blank=False)

    # Other
    dominionVictoryScore = models.BigIntegerField(blank=False)
    vilemawKills = models.BigIntegerField(blank=False)

    def __str__(self):
        team = 'Blue' if self.teamId == 100 else 'Red'
        return str(self.match) + ' - Team: ' + team

class Player(models.Model):

    # Participant Identity
    match = models.ForeignKey(Match, related_name='Players', on_delete=models.CASCADE, blank=False)
    summoner = models.ForeignKey(Summoner, related_name='Players', on_delete=models.SET_NULL, blank=False, null=True)
    currentPlatformId = models.CharField(max_length=255, blank=False)
    platformId = models.CharField(max_length=255, blank=False)
    matchHistoryUri = models.CharField(max_length=255, blank=False)
    participantId = models.BigIntegerField(blank=False)

    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)

    # Participant Stats
    champion = models.ForeignKey(Champion, related_name='Players', on_delete=models.SET_NULL, blank=False, null=True)
    spell1Id = models.BigIntegerField(blank=False)
    spell2Id = models.BigIntegerField(blank=False)
    neutralMinionsKilledTeamJungle = models.BigIntegerField(blank=False)
    visionScore = models.BigIntegerField(blank=False)
    magicDamageDealtToChampions = models.BigIntegerField(blank=False)
    largestMultiKill = models.BigIntegerField(blank=False)
    totalTimeCrowdControlDealt = models.BigIntegerField(blank=False)
    longestTimeSpentLiving = models.BigIntegerField(blank=False)
    perk1Var1 = models.BigIntegerField(blank=False)
    perk1Var3 = models.BigIntegerField(blank=False)
    perk1Var2 = models.BigIntegerField(blank=False)
    tripleKills = models.BigIntegerField(blank=False)
    perk5 = models.BigIntegerField(blank=False)
    perk4 = models.BigIntegerField(blank=False)
    playerScore9 = models.BigIntegerField(blank=False)
    playerScore8 = models.BigIntegerField(blank=False)
    kills = models.BigIntegerField(blank=False)
    playerScore1 = models.BigIntegerField(blank=False)
    playerScore0 = models.BigIntegerField(blank=False)
    playerScore3 = models.BigIntegerField(blank=False)
    playerScore2 = models.BigIntegerField(blank=False)
    playerScore5 = models.BigIntegerField(blank=False)
    playerScore4 = models.BigIntegerField(blank=False)
    playerScore7 = models.BigIntegerField(blank=False)
    playerScore6 = models.BigIntegerField(blank=False)
    perk5Var1 = models.BigIntegerField(blank=False)
    perk5Var3 = models.BigIntegerField(blank=False)
    perk5Var2 = models.BigIntegerField(blank=False)
    totalScoreRank = models.BigIntegerField(blank=False)
    neutralMinionsKilled = models.BigIntegerField(blank=False)
    statPerk1 = models.BigIntegerField(blank=False)
    statPerk0 = models.BigIntegerField(blank=False)
    damageDealtToTurrets = models.BigIntegerField(blank=False)
    physicalDamageDealtToChampions = models.BigIntegerField(blank=False)
    damageDealtToObjectives = models.BigIntegerField(blank=False)
    perk2Var2 = models.BigIntegerField(blank=False)
    perk2Var3 = models.BigIntegerField(blank=False)
    totalUnitsHealed = models.BigIntegerField(blank=False)
    perk2Var1 = models.BigIntegerField(blank=False)
    perk4Var1 = models.BigIntegerField(blank=False)
    totalDamageTaken = models.BigIntegerField(blank=False)
    perk4Var3 = models.BigIntegerField(blank=False)
    wardsKilled = models.BigIntegerField(blank=False)
    largestCriticalStrike = models.BigIntegerField(blank=False)
    largestKillingSpree = models.BigIntegerField(blank=False)
    quadraKills = models.BigIntegerField(blank=False)
    magicDamageDealt = models.BigIntegerField(blank=False)
    firstBloodAssist = models.BooleanField(default=False)
    item2 = models.BigIntegerField(blank=False)
    item3 = models.BigIntegerField(blank=False)
    item0 = models.BigIntegerField(blank=False)
    item1 = models.BigIntegerField(blank=False)
    item6 = models.BigIntegerField(blank=False)
    item4 = models.BigIntegerField(blank=False)
    item5 = models.BigIntegerField(blank=False)
    perk1 = models.BigIntegerField(blank=False)
    perk0 = models.BigIntegerField(blank=False)
    perk3 = models.BigIntegerField(blank=False)
    perk2 = models.BigIntegerField(blank=False)
    perk3Var3 = models.BigIntegerField(blank=False)
    perk3Var2 = models.BigIntegerField(blank=False)
    perk3Var1 = models.BigIntegerField(blank=False)
    damageSelfMitigated = models.BigIntegerField(blank=False)
    magicalDamageTaken = models.BigIntegerField(blank=False)
    perk0Var2 = models.BigIntegerField(blank=False)
    firstInhibitorKill = models.BooleanField(default=False)
    trueDamageTaken = models.BigIntegerField(blank=False)
    assists = models.BigIntegerField(blank=False)
    perk4Var2 = models.BigIntegerField(blank=False)
    goldSpent = models.BigIntegerField(blank=False)
    trueDamageDealt = models.BigIntegerField(blank=False)
    participantId = models.BigIntegerField(blank=False)
    physicalDamageDealt = models.BigIntegerField(blank=False)
    sightWardsBoughtInGame = models.BigIntegerField(blank=False)
    totalDamageDealtToChampions = models.BigIntegerField(blank=False)
    physicalDamageTaken = models.BigIntegerField(blank=False)
    totalPlayerScore = models.BigIntegerField(blank=False)
    win = models.BooleanField(default=False)
    objectivePlayerScore = models.BigIntegerField(blank=False)
    totalDamageDealt = models.BigIntegerField(blank=False)
    neutralMinionsKilledEnemyJungle = models.BigIntegerField(blank=False)
    deaths = models.BigIntegerField(blank=False)
    wardsPlaced = models.BigIntegerField(blank=False)
    perkPrimaryStyle = models.BigIntegerField(blank=False)
    perkSubStyle = models.BigIntegerField(blank=False)
    turretKills = models.BigIntegerField(blank=False)
    firstBloodKill = models.BooleanField(default=False)
    trueDamageDealtToChampions = models.BigIntegerField(blank=False)
    goldEarned = models.BigIntegerField(blank=False)
    killingSprees = models.BigIntegerField(blank=False)
    unrealKills = models.BigIntegerField(blank=False)
    firstTowerAssist = models.BooleanField(default=False)
    firstTowerKill = models.BooleanField(default=False)
    champLevel = models.BigIntegerField(blank=False)
    doubleKills = models.BigIntegerField(blank=False)
    inhibitorKills = models.BigIntegerField(blank=False)
    firstInhibitorAssist = models.BooleanField(default=False)
    perk0Var1 = models.BigIntegerField(blank=False)
    combatPlayerScore = models.BigIntegerField(blank=False)
    perk0Var3 = models.BigIntegerField(blank=False)
    visionWardsBoughtInGame = models.BigIntegerField(blank=False)
    pentaKills = models.BigIntegerField(blank=False)
    totalHeal = models.BigIntegerField(blank=False)
    totalMinionsKilled = models.BigIntegerField(blank=False)
    timeCCingOthers = models.BigIntegerField(blank=False)
    statPerk2 = models.BigIntegerField(blank=False)

    def __str__(self):
        return str(self.match) + ' - Player: ' + str(self.summoner)
