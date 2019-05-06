import graphene
import timeago
from django.utils import timezone
from graphene_django.types import DjangoObjectType
from dashboard.models import Player, Match, Summoner, RankedTier, Champion, Item, Rune, SummonerSpell, Team
from django.db.models import Sum


class MatchType(DjangoObjectType):
    queue = graphene.String()
    timeago = graphene.String()
    game_duration_time = graphene.String()

    class Meta:
        model = Match

    def resolve_queue(self, info, **kwargs):
        return self.get_queueId_display()

    def resolve_timeago(self, info, **kwargs):
        return timeago.format(self.timestamp, timezone.now())

    def resolve_game_duration_time(self, info, **kwargs):
        duration_seconds = self.gameDuration % 60
        duration_minutes = (self.gameDuration - duration_seconds) / 60
        result = str(int(duration_minutes)) + 'm ' + str(duration_seconds) + 's '
        return result


class ChampionType(DjangoObjectType):
    class Meta:
        model = Champion


class RankedTier(DjangoObjectType):
    class Meta:
        model = RankedTier


class Ranked(graphene.ObjectType):
    tier = graphene.String()
    rank = graphene.String()
    rank_number = graphene.Int()
    lp = graphene.Int()
    league_name = graphene.String()
    wins = graphene.Int()
    losses = graphene.Int()
    ring_values = graphene.String()

    def resolve_ring_values(self, info, **kwargs):
        leftover = 100 - self.lp
        return str(self.lp) + ' ' + str(leftover)

    def resolve_rank_number(self, info, **kwargs):
        if self.rank == 'IV':
            number = 4
        elif self.rank == 'III':
            number = 3
        elif self.rank == 'II':
            number = 2
        elif self.rank == 'I':
            number = 1
        else:
            number = None

        return number


class SummonerType(DjangoObjectType):
    last_updated = graphene.String()
    solo_rank_number = graphene.Int()
    flex_sr_ranked_number = graphene.Int()
    flex_tt_ranked_number = graphene.Int()
    ranked_solo = graphene.Field(Ranked)
    ranked_flex_5 = graphene.Field(Ranked)
    ranked_flex_3 = graphene.Field(Ranked)

    def resolve_ranked_solo(self, info, **kwargs):
        if self.soloQ_tier:
            return Ranked(
                tier=self.soloQ_tier,
                rank=self.soloQ_rank,
                lp=self.soloQ_leaguePoints,
                league_name=self.soloQ_leagueName,
                wins=self.soloQ_wins,
                losses=self.soloQ_losses
            )
        else:
            return None

    def resolve_ranked_flex_5(self, info, **kwargs):
        if self.flexSR_tier:
            return Ranked(
                tier=self.flexSR_tier,
                rank=self.flexSR_rank,
                lp=self.flexSR_leaguePoints,
                league_name=self.flexSR_leagueName,
                wins=self.flexSR_wins,
                losses=self.flexSR_losses
            )
        else:
            return None

    def resolve_ranked_flex_3(self, info, **kwargs):
        if self.flexTT_tier:
            return Ranked(
                tier=self.flexTT_tier,
                rank=self.flexTT_rank,
                lp=self.flexTT_leaguePoints,
                league_name=self.flexTT_leagueName,
                wins=self.flexTT_wins,
                losses=self.flexTT_losses
            )
        else:
            return None

    class Meta:
        model = Summoner

    def resolve_last_updated(self, info, **kwargs):
        return timeago.format(self.date_updated, timezone.now())


class RuneType(DjangoObjectType):
    class Meta:
        model = Rune


class ItemType(DjangoObjectType):
    class Meta:
        model = Item

class TeamType(DjangoObjectType):
    class Meta:
        model = Team

class SummonerSpellType(DjangoObjectType):
    class Meta:
        model = SummonerSpell


class PlayerType(DjangoObjectType):
    kda_average = graphene.String()
    cs_pmin = graphene.Float()
    perk_sub_style = graphene.String()
    win = graphene.String()
    kill_participation = graphene.String()

    class Meta:
        model = Player

    def resolve_kda_average(self, info, **kwargs):
        average = (self.kills + self.assists) / self.deaths
        return round(average, 2)

    def resolve_cs_pmin(self, info, **kwargs):
        duration_seconds = self.match.gameDuration % 60
        duration_minutes = (self.match.gameDuration - duration_seconds) / 60
        return round(self.totalMinionsKilled / (duration_minutes + (duration_seconds / 60)), 1)

    def resolve_perk_sub_style(self, info, **kwargs):
        if self.perkSubStyle == 8000:
            return '7201_Precision'
        elif self.perkSubStyle == 8100:
            return '7200_Domination'
        elif self.perkSubStyle == 8200:
            return '7202_Sorcery'
        elif self.perkSubStyle == 8300:
            return '7203_Whimsy'
        elif self.perkSubStyle == 8400:
            return '7204_Resolve'

    def resolve_win(self, info, **kwargs):
        return 'W' if self.win else 'L'

    def resolve_kill_participation(self, info, **kwargs):
        total_kills = Player.objects.filter(match=self.match, team=self.team).aggregate(Sum('kills')).get('kills__sum', 0)

        return str(int(((self.kills + self.assists) / total_kills) * 100)) + '%'


class Query(object):
    match = graphene.Field(MatchType, gameId=graphene.Int())
    all_matches = graphene.List(MatchType)

    player = graphene.Field(PlayerType, summonerId=graphene.Int())
    summoner_players = graphene.List(PlayerType,
                                     summonerName=graphene.String(),
                                     games=graphene.Int())
    all_players = graphene.List(PlayerType)

    summoner = graphene.Field(SummonerType, summonerName=graphene.String())
    all_summoners = graphene.List(SummonerType)

    def resolve_summoner(self, info, **kwargs):
        summonerName = kwargs.get('summonerName')

        if summonerName:
            return Summoner.objects.get(summonerName__iexact=summonerName)

    def resolve_all_summoners(self, info, **kwargs):
        return Summoner.objects.all()

    def resolve_match(self, info, **kwargs):
        game_id = kwargs.get('gameId')

        if game_id:
            return Match.objects.get(gameId=game_id)

    def resolve_summoner_players(self, info, **kwargs):
        summoner_name = kwargs.get('summonerName')
        games = kwargs.get('games')

        summoner = Summoner.objects.get(summonerName=summoner_name)
        return Player.objects.filter(summoner=summoner).order_by('-match__timestamp').select_related('champion')[:games]

    def resolve_all_matches(self, info, **kwargs):
        return Match.objects.all()

    def resolve_all_players(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Player.objects.select_related('match', 'summoner').all()[:10]
