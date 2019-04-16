from django.db import models
from django.contrib.auth.models import User
from s3direct.fields import S3DirectField
import json

class Setting(models.Model):
    name = models.CharField(max_length=255, blank=False)
    latestVersion = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(User, related_name="Profiles", on_delete=models.CASCADE, blank=False)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.CharField(max_length=255, blank=False)
    avatar = S3DirectField(dest='profiles', null=True, blank=True)
    friends = models.ManyToManyField('Profile', related_name='Friends')

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_modified = models.DateTimeField(auto_now=True, blank=False)

    def __str__(self):
        return self.user.username

class RankedTier(models.Model):
    key = models.CharField(primary_key=True, max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    order = models.IntegerField()

class ChatRoom(models.Model):
    members = models.ManyToManyField('Profile', related_name='Members')
    roomId = models.CharField(max_length=255, blank=False)

    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_updated = models.DateTimeField(blank=False)

class SummonerSpell(models.Model):
    version = models.CharField(max_length=255, null=True)
    key = models.IntegerField(blank=False, unique=True, primary_key=True)
    summonerSpellId = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    tooltip = models.TextField(null=True)
    maxrank = models.IntegerField(null=True)
    cooldown = models.IntegerField(null=True)
    cooldownBurn = models.CharField(max_length=255, null=True)
    cost = models.IntegerField(null=True)
    costBurn = models.CharField(max_length=255, null=True)
    costType = models.CharField(max_length=255, null=True)
    summonerLevel = models.IntegerField(null=True)
    maxammo = models.CharField(max_length=255, null=True)
    range = models.IntegerField(null=True)
    rangeBurn = models.CharField(max_length=255, null=True)
    image_full = models.CharField(max_length=255, null=True)
    image_sprite = models.CharField(max_length=255, null=True)
    image_group = models.CharField(max_length=255, null=True)
    image_x = models.IntegerField(null=True)
    image_y = models.IntegerField(null=True)
    image_w = models.IntegerField(null=True)
    image_h = models.IntegerField(null=True)
    resource = models.CharField(max_length=255, null=True)

    # Some fields have been removed for simplicity sake. Keep this in mind, they may need to be added later.

    def __str__(self):
        return str(self.name)

class Rune(models.Model):
    version = models.CharField(max_length=255, blank=False)
    runeId = models.IntegerField(blank=False, unique=True, primary_key=True)
    key = models.CharField(max_length=255, blank=False)
    icon = models.CharField(max_length=255, blank=False)
    name = models.CharField(max_length=255, blank=False)
    shortDesc = models.TextField(blank=False)
    longDesc = models.TextField(blank=False)

    def __str__(self):
        return str(self.name)


class Item(models.Model):
    version = models.CharField(max_length=255)
    itemId = models.IntegerField(blank=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=False)
    colloq = models.CharField(max_length=255)
    plaintext = models.CharField(max_length=255)
    built_into = models.ManyToManyField('Item', related_name='item_into')
    built_from = models.ManyToManyField('Item', related_name='item_from')
    consumed = models.BooleanField(default=False)
    stacks = models.IntegerField(default=1)
    depth = models.IntegerField(default=1)
    consumeOnFull = models.BooleanField(default=False)
    specialRecipe = models.IntegerField(default=0)
    inStore = models.BooleanField(default=True)
    hideFromAll = models.BooleanField(default=False)
    requiredChampion = models.CharField(max_length=255)
    requiredAlly = models.CharField(max_length=255)

    image_full = models.CharField(max_length=255)
    image_sprite = models.CharField(max_length=255)
    image_group = models.CharField(max_length=255)
    image_x = models.IntegerField(default=0)
    image_y = models.IntegerField(default=0)
    image_w = models.IntegerField(default=0)
    image_h = models.IntegerField(default=0)

    gold_base = models.IntegerField(default=0)
    gold_purchasable = models.BooleanField(default=True)
    gold_total = models.IntegerField(default=0)
    gold_sell = models.IntegerField(default=0)

    tags = models.CharField(max_length=255)

    maps_1 = models.BooleanField(default=True)
    maps_8 = models.BooleanField(default=True)
    maps_10 = models.BooleanField(default=True)
    maps_11 = models.BooleanField(default=True)
    maps_12 = models.BooleanField(default=True)

    FlatHPPoolMod = models.IntegerField(default=0)
    rFlatHPModPerLevel = models.IntegerField(default=0)
    FlatMPPoolMod = models.IntegerField(default=0)
    rFlatMPModPerLevel = models.IntegerField(default=0)
    PercentHPPoolMod = models.IntegerField(default=0)
    PercentMPPoolMod = models.IntegerField(default=0)
    FlatHPRegenMod = models.IntegerField(default=0)
    rFlatHPRegenModPerLevel = models.IntegerField(default=0)
    PercentHPRegenMod = models.IntegerField(default=0)
    FlatMPRegenMod = models.IntegerField(default=0)
    rFlatMPRegenModPerLevel = models.IntegerField(default=0)
    PercentMPRegenMod = models.IntegerField(default=0)
    FlatArmorMod = models.IntegerField(default=0)
    rFlatArmorModPerLevel = models.IntegerField(default=0)
    PercentArmorMod = models.IntegerField(default=0)
    rFlatArmorPenetrationMod = models.IntegerField(default=0)
    rFlatArmorPenetrationModPerLevel = models.IntegerField(default=0)
    rPercentArmorPenetrationMod = models.IntegerField(default=0)
    rPercentArmorPenetrationModPerLevel = models.IntegerField(default=0)
    FlatPhysicalDamageMod = models.IntegerField(default=0)
    rFlatPhysicalDamageModPerLevel = models.IntegerField(default=0)
    PercentPhysicalDamageMod = models.IntegerField(default=0)
    FlatMagicDamageMod = models.IntegerField(default=0)
    rFlatMagicDamageModPerLevel = models.IntegerField(default=0)
    PercentMagicDamageMod = models.IntegerField(default=0)
    FlatMovementSpeedMod = models.IntegerField(default=0)
    rFlatMovementSpeedModPerLevel = models.IntegerField(default=0)
    PercentMovementSpeedMod = models.IntegerField(default=0)
    rPercentMovementSpeedModPerLevel = models.IntegerField(default=0)
    FlatAttackSpeedMod = models.IntegerField(default=0)
    PercentAttackSpeedMod = models.IntegerField(default=0)
    rPercentAttackSpeedModPerLevel = models.IntegerField(default=0)
    rFlatDodgeMod = models.IntegerField(default=0)
    rFlatDodgeModPerLevel = models.IntegerField(default=0)
    PercentDodgeMod = models.IntegerField(default=0)
    FlatCritChanceMod = models.IntegerField(default=0)
    rFlatCritChanceModPerLevel = models.IntegerField(default=0)
    PercentCritChanceMod = models.IntegerField(default=0)
    FlatCritDamageMod = models.IntegerField(default=0)
    rFlatCritDamageModPerLevel = models.IntegerField(default=0)
    PercentCritDamageMod = models.IntegerField(default=0)
    FlatBlockMod = models.IntegerField(default=0)
    PercentBlockMod = models.IntegerField(default=0)
    FlatSpellBlockMod = models.IntegerField(default=0)
    rFlatSpellBlockModPerLevel = models.IntegerField(default=0)
    PercentSpellBlockMod = models.IntegerField(default=0)
    FlatEXPBonus = models.IntegerField(default=0)
    PercentEXPBonus = models.IntegerField(default=0)
    rPercentCooldownMod = models.IntegerField(default=0)
    rPercentCooldownModPerLevel = models.IntegerField(default=0)
    rFlatTimeDeadMod = models.IntegerField(default=0)
    rFlatTimeDeadModPerLevel = models.IntegerField(default=0)
    rPercentTimeDeadMod = models.IntegerField(default=0)
    rPercentTimeDeadModPerLevel = models.IntegerField(default=0)
    rFlatGoldPer10Mod = models.IntegerField(default=0)
    rFlatMagicPenetrationMod = models.IntegerField(default=0)
    rFlatMagicPenetrationModPerLevel = models.IntegerField(default=0)
    rPercentMagicPenetrationMod = models.IntegerField(default=0)
    rPercentMagicPenetrationModPerLevel = models.IntegerField(default=0)
    FlatEnergyRegenMod = models.IntegerField(default=0)
    rFlatEnergyRegenModPerLevel = models.IntegerField(default=0)
    FlatEnergyPoolMod = models.IntegerField(default=0)
    rFlatEnergyModPerLevel = models.IntegerField(default=0)
    PercentLifeStealMod = models.IntegerField(default=0)
    PercentSpellVampMod = models.IntegerField(default=0)

    def set_tags(self, x):
        self.tags = json.dumps(x)

    def get_tags(self):
        return json.loads(self.tags)

    def __str__(self):
        return str(self.name)


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

    TIERS = (
        ('CHALLENGER', 'Challenger'),
        ('GRANDMASTER', 'Grandmaster'),
        ('MASTER', 'Master'),
        ('DIAMOND', 'Diamond'),
        ('PLATINUM', 'Platinum'),
        ('GOLD', 'Gold'),
        ('SILVER', 'Silver'),
        ('BRONZE', 'Bronze'),
        ('IRON', 'Iron'),
    )

    # SoloQ
    soloQ_leagueId = models.CharField(max_length=255, blank=True)
    soloQ_leagueName = models.CharField(max_length=255, blank=True)
    soloQ_tier = models.CharField(max_length=20, choices=TIERS, null=True, blank=True)
    soloQ_hotStreak = models.BooleanField(default=False)
    soloQ_wins = models.BigIntegerField(null=True, blank=True, default=0)
    soloQ_losses = models.BigIntegerField(null=True, blank=True, default=0)
    soloQ_veteran = models.BooleanField(default=False)
    soloQ_rank = models.CharField(max_length=255, null=True, blank=True)
    soloQ_inactive = models.BooleanField(default=False)
    soloQ_freshBlood = models.BooleanField(default=False)
    soloQ_leaguePoints = models.BigIntegerField(null=True, blank=True, default=0)

    # Flex SR
    flexSR_leagueId = models.CharField(max_length=255, blank=True)
    flexSR_leagueName = models.CharField(max_length=255, blank=True)
    flexSR_tier = models.CharField(max_length=20, choices=TIERS, null=True, blank=True)
    flexSR_hotStreak = models.BooleanField(default=False)
    flexSR_wins = models.BigIntegerField(null=True, blank=True, default=0)
    flexSR_losses = models.BigIntegerField(null=True, blank=True, default=0)
    flexSR_veteran = models.BooleanField(default=False)
    flexSR_rank = models.CharField(max_length=255, null=True, blank=True)
    flexSR_inactive = models.BooleanField(default=False)
    flexSR_freshBlood = models.BooleanField(default=False)
    flexSR_leaguePoints = models.BigIntegerField(null=True, blank=True, default=0)

    # Flex TT
    flexTT_leagueId = models.CharField(max_length=255, blank=True)
    flexTT_leagueName = models.CharField(max_length=255, blank=True)
    flexTT_tier = models.CharField(max_length=20, choices=TIERS, null=True, blank=True)
    flexTT_hotStreak = models.BooleanField(default=False)
    flexTT_wins = models.BigIntegerField(null=True, blank=True, default=0)
    flexTT_losses = models.BigIntegerField(null=True, blank=True, default=0)
    flexTT_veteran = models.BooleanField(default=False)
    flexTT_rank = models.CharField(max_length=255, null=True, blank=True)
    flexTT_inactive = models.BooleanField(default=False)
    flexTT_freshBlood = models.BooleanField(default=False)
    flexTT_leaguePoints = models.BigIntegerField(null=True, blank=True, default=0)

    # System
    date_created = models.DateTimeField(auto_now_add=True, blank=False)
    date_updated = models.DateTimeField(null=True)

    def __str__(self):
        return self.summonerName

    def __unicode__(self):
        return self.summonerName

class Match(models.Model):
    # IDs
    platformId = models.CharField(max_length=255, blank=False) # Server
    gameId = models.BigIntegerField(blank=False)
    QUEUES = (
        (0, 'Custom'),
        (72, '1v1 Snowdown Showdown'),
        (73, '2v2 Snowdown Showdown'),
        (75, '6v6 Hexakill'),
        (76, 'Ultra Rapid Fire'),
        (78, 'One For All: Mirror Mode'),
        (83, 'Co-op vs AI Ultra Rapid Fire'),
        (98, '6v6 Hexakill'),
        (100, '5v5 ARAM'),
        (310, 'Nemesis'),
        (313, 'Black Market Brawlers'),
        (317, 'Definitely Not Dominion'),
        (325, 'All Random'),
        (400, '5v5 Draft Pick'),
        (420, '5v5 Ranked Solo'),
        (430, '5v5 Blind Pick'),
        (440, '5v5 Ranked Flex'),
        (450, '5v5 ARAM'),
        (460, '3v3 Blind Pick'),
        (470, '3v3 Ranked Flex'),
        (600, 'Blood Hunt Assassin'),
        (610, 'Dark Star: Singularity'),
        (700, 'Clash'),
        (800, 'Co-op vs. AI Intermediate Bot'),
        (810, 'Co-op vs. AI Intro Bot'),
        (820, 'Co-op vs. AI Beginner Bot'),
        (830, 'Co-op vs. AI Intro Bot'),
        (840, 'Co-op vs. AI Beginner Bot'),
        (850, 'Co-op vs. AI Intermediate Bot'),
        (900, 'ARURF'),
        (910, 'Ascension'),
        (920, 'Legend of the Poro King'),
        (940, 'Nexus Siege'),
        (950, 'Doom Bots Voting'),
        (960, 'Doom Bots Standard'),
        (980, 'Star Guardian Invasion: Normal'),
        (990, 'Star Guardian Invasion: Onslaught'),
        (1000, 'PROJECT: Hunters'),
        (1010, 'Snow ARURF'),
        (1020, 'One for All'),
        (1030, 'Odyssey Extraction: Intro'),
        (1040, 'Odyssey Extraction: Cadet'),
        (1050, 'Odyssey Extraction: Crewmember'),
        (1060, 'Odyssey Extraction: Captain'),
        (1070, 'Odyssey Extraction: Onslaught'),
        (1200, 'Nexus Blitz'),
    )
    queueId = models.IntegerField(choices=QUEUES, null=True, blank=True)
    SEASONS = (
        (0, 'PRESEASON 3'),
        (1, 'SEASON 3'),
        (2, 'PRESEASON 2014'),
        (3, 'SEASON 2014'),
        (4, 'PRESEASON 2015'),
        (5, 'SEASON 2015'),
        (6, 'PRESEASON 2016'),
        (7, 'SEASON 2016'),
        (8, 'PRESEASON 2017'),
        (9, 'SEASON 2017'),
        (10, 'PRESEASON 2018'),
        (11, 'SEASON 2018'),
        (12, 'PRESEASON 2019'),
        (13, 'SEASON 2019'),
    )
    seasonId = models.IntegerField(choices=SEASONS, null=True, blank=True)
    MAPS = (
        (1, 'Summoner\'s Rift - Summer'),
        (2, 'Summoner\'s Rift - Autumn'),
        (3, 'The Proving Grounds'),
        (4, 'Twisted Treeline - Original'),
        (8, 'The Crystal Scar'),
        (10, 'Twisted Treeline'),
        (11, 'Summoner\'s Rift'),
        (12, 'Howling Abyss'),
        (14, 'Butcher\'s Bridge'),
        (16, 'Cosmic Ruins'),
        (18, 'Valoran City Park'),
        (19, 'Substructure 43'),
        (20, 'Crash Site'),
        (21, 'Nexus Blitz'),
    )
    mapId = models.IntegerField(choices=MAPS, null=True, blank=True)

    # Players
    players = models.ManyToManyField('Summoner', related_name='Matches')

    # Match Information
    gameMode = models.CharField(max_length=255, blank=False)
    gameType = models.CharField(max_length=255, blank=False)
    gameVersion = models.CharField(max_length=255, blank=False)
    gameDuration = models.BigIntegerField(blank=False)
    timestamp = models.DateTimeField(blank=False)

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
    spell1Id = models.ForeignKey(SummonerSpell, related_name='Player_SSpells_1', on_delete=models.SET_NULL, blank=False, null=True)
    spell2Id = models.ForeignKey(SummonerSpell, related_name='Player_SSPells_2', on_delete=models.SET_NULL, blank=False, null=True)
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
    perk5 = models.ForeignKey(Rune, related_name='Player_Runes_6', on_delete=models.SET_NULL, blank=False, null=True)
    perk4 = models.ForeignKey(Rune, related_name='Player_Runes_5', on_delete=models.SET_NULL, blank=False, null=True)
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
    item2 = models.ForeignKey(Item, related_name='Player_Items_3', on_delete=models.SET_NULL, null=True)
    item3 = models.ForeignKey(Item, related_name='Player_Items_4', on_delete=models.SET_NULL, null=True)
    item0 = models.ForeignKey(Item, related_name='Player_Items_1', on_delete=models.SET_NULL, null=True)
    item1 = models.ForeignKey(Item, related_name='Player_Items_2', on_delete=models.SET_NULL, null=True)
    item6 = models.ForeignKey(Item, related_name='Player_Items_7', on_delete=models.SET_NULL, null=True)
    item4 = models.ForeignKey(Item, related_name='Player_Items_5', on_delete=models.SET_NULL, null=True)
    item5 = models.ForeignKey(Item, related_name='Player_Items_6', on_delete=models.SET_NULL, null=True)
    perk1 = models.ForeignKey(Rune, related_name='Player_Runes_2', on_delete=models.SET_NULL, blank=False, null=True)
    perk0 = models.ForeignKey(Rune, related_name='Player_Runes_1', on_delete=models.SET_NULL, blank=False, null=True)
    perk3 = models.ForeignKey(Rune, related_name='Player_Runes_4', on_delete=models.SET_NULL, blank=False, null=True)
    perk2 = models.ForeignKey(Rune, related_name='Player_Runes_3', on_delete=models.SET_NULL, blank=False, null=True)
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
