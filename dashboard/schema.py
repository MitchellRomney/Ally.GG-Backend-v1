import graphene
import timeago
from django.utils import timezone
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from dashboard.models import Player, Match, Summoner, RankedTier, Champion, Item, Rune, SummonerSpell, Team, Profile, \
    ImprovementLog, AccessCode
from django.db.models import Sum
from dashboard.functions.summoners import add_summoner, update_summoner, get_all_ranked_summoners
from dashboard.functions.match import fetch_match_list, create_match
from graphene_django.converter import convert_django_field
from graphql_jwt.decorators import login_required
from s3direct.fields import S3DirectField
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import send_mail
from dashboard.functions.users import generate_access_code, account_activation_token
from django.db import IntegrityError



@convert_django_field.register(S3DirectField)
def convert_s3_direct_field_to_string(field, registry=None):
    return graphene.String()


class FunctionType(graphene.ObjectType):
    success = graphene.Boolean()


class ImprovementLogType(DjangoObjectType):
    class Meta:
        model = ImprovementLog


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


class AccessKeyType(DjangoObjectType):
    class Meta:
        model = AccessCode


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


class UserType(DjangoObjectType):
    class Meta:
        model = User


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile


class Opponent(DjangoObjectType):
    class Meta:
        model = Player


class PlayerType(DjangoObjectType):
    kda_average = graphene.String()
    cs_pmin = graphene.Float()
    perk_sub_style = graphene.String()
    kill_participation = graphene.String()
    lane_opponent = graphene.List(Opponent)
    lane = graphene.String()

    class Meta:
        model = Player

    def resolve_lane(self, info, **kwargs):
        if self.lane == 'UNKNOWN':
            self.lane = 'NONE'
            player = Player.objects.get(id=self.id)
            player.save()
            return 'NONE'

        else:
            return self.lane

    def resolve_lane_opponent(self, info, **kwargs):
        opponents = []

        if self.lane != 'UNKNOWN' and self.lane != 'NONE':
            if Player.objects.filter(match=self.match, lane=self.lane).exclude(team=self.team).count() != 0:
                opponent_list = Player.objects.filter(match=self.match, lane=self.lane).exclude(team=self.team)
                for opponent in opponent_list:
                    opponents.append(opponent)

            return opponents
        else:
            return None

    def resolve_kda_average(self, info, **kwargs):
        if self.deaths != 0:
            average = (self.kills + self.assists) / self.deaths
            return round(average, 2)
        else:
            return round(self.kills + self.assists, 2)

    def resolve_cs_pmin(self, info, **kwargs):
        if self.totalMinionsKilled != 0:
            duration_seconds = self.match.gameDuration % 60
            duration_minutes = (self.match.gameDuration - duration_seconds) / 60
            return round(self.totalMinionsKilled / (duration_minutes + (duration_seconds / 60)), 1)
        else:
            return 0.0

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

    def resolve_kill_participation(self, info, **kwargs):
        total_kills = Player.objects.filter(match=self.match, team=self.team).aggregate(Sum('kills')).get('kills__sum',
                                                                                                          0)
        if total_kills != 0:
            return str(int(((self.kills + self.assists) / total_kills) * 100)) + '%'
        else:
            return '0%'


class Query(object):
    # Match Objects
    match = graphene.Field(MatchType, gameId=graphene.Int())
    all_matches = graphene.List(MatchType)

    # Player Objects
    player = graphene.Field(PlayerType, summonerId=graphene.String(), gameId=graphene.Int())
    summoner_players = graphene.List(PlayerType,
                                     summonerName=graphene.String(),
                                     games=graphene.Int())
    all_players = graphene.List(PlayerType)

    # User / Profile Objects
    user = graphene.Field(UserType, username=graphene.String(), id=graphene.Int())

    # Improvement Log Objects
    log = graphene.Field(ImprovementLogType, summonerId=graphene.String(), gameId=graphene.Int())

    # Champion Objects
    champion_search = graphene.List(ChampionType, entry=graphene.String())

    # Access Key Objects
    key = graphene.Field(AccessKeyType, key=graphene.String())

    # Summoner Objects
    summoner = graphene.Field(SummonerType, summonerName=graphene.String())
    get_summoners = graphene.List(SummonerType, summonerIds=graphene.List(graphene.String))
    summoner_search = graphene.List(SummonerType, entry=graphene.String())
    latest_updated_summoners = graphene.List(SummonerType)
    top_summoners = graphene.List(SummonerType)
    all_summoners = graphene.List(SummonerType)

    @staticmethod
    def resolve_key(self, info, **kwargs):
        key = kwargs.get('key')

        if key:
            return AccessCode.objects.get(key=key)

    @staticmethod
    @login_required
    def resolve_summoner(self, info, **kwargs):
        summoner_name = kwargs.get('summonerName')

        if summoner_name:
            return Summoner.objects.get(summonerName__iexact=summoner_name)

    @staticmethod
    def resolve_player(self, info, **kwargs):
        summoner_id = kwargs.get('summonerId')
        game_id = kwargs.get('gameId')

        return Player.objects.get(summoner__summonerId=summoner_id, match__gameId=game_id)

    @staticmethod
    def resolve_get_summoners(self, info, **kwargs):
        summoner_ids = kwargs.get('summonerIds')

        return Summoner.objects.filter(summonerId__in=summoner_ids)

    @staticmethod
    def resolve_summoner_search(self, info, **kwargs):
        entry = kwargs.get('entry')

        if entry:
            return Summoner.objects.filter(summonerName__icontains=entry)

    @staticmethod
    def resolve_champion_search(self, info, **kwargs):
        entry = kwargs.get('entry')

        if entry:
            return Champion.objects.filter(name__icontains=entry)

    @staticmethod
    def resolve_log(self, info, **kwargs):
        summoner_id = kwargs.get('summonerId')
        game_id = kwargs.get('gameId')

        return ImprovementLog.objects.get(summoner__summonerId=summoner_id, match__gameId=game_id)

    @staticmethod
    def resolve_latest_updated_summoners(self, info, **kwargs):
        return Summoner.objects.order_by('-date_updated').exclude(date_updated=None)[:100]

    @staticmethod
    def resolve_top_summoners(self, info, **kwargs):
        summoners = Summoner.objects.all()
        top_summoners = summoners.select_related('soloQ_tier').exclude(soloQ_tier=None)
        return top_summoners.order_by('soloQ_tier__order', 'soloQ_rank', '-soloQ_leaguePoints')[:100]

    @staticmethod
    def resolve_all_summoners(self, info, **kwargs):
        return Summoner.objects.all()

    @staticmethod
    def resolve_match(self, info, **kwargs):
        game_id = kwargs.get('gameId')

        if game_id:
            return Match.objects.get(gameId=game_id)

    @staticmethod
    def resolve_summoner_players(self, info, **kwargs):
        summoner_name = kwargs.get('summonerName')
        games = kwargs.get('games')

        summoner = Summoner.objects.get(summonerName__iexact=summoner_name)
        return Player.objects.filter(summoner=summoner).order_by('-match__timestamp').select_related('champion')[:games]

    @staticmethod
    def resolve_all_matches(self, info, **kwargs):
        return Match.objects.all()

    @staticmethod
    def resolve_all_players(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Player.objects.select_related('match', 'summoner').all()[:10]

    @staticmethod
    def resolve_user(self, info, **kwargs):
        username = kwargs.get('username')
        user_id = kwargs.get('id')
        if user_id is not None:
            return User.objects.get(id=user_id)
        else:
            return User.objects.get(username=username)


class CreateSummoner(graphene.Mutation):
    class Arguments:
        summonerName = graphene.String()

    created = graphene.Boolean()
    message = graphene.String()
    summoner = graphene.Field(SummonerType)

    @staticmethod
    def mutate(root, info, summonerName):
        created = False
        summoner = None

        add_response = add_summoner('summonerName', summonerName)
        message = add_response['message']

        if not add_response['isError']:
            update_response = update_summoner(add_response['summonerId'])

            created = True
            summoner = update_response['summoner']

        return CreateSummoner(created=created, summoner=summoner, message=message)


class UpdateSummoner(graphene.Mutation):
    class Arguments:
        id = graphene.String()

    updated = graphene.Boolean()
    message = graphene.String()
    summoner = graphene.Field(SummonerType)
    new_matches = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, id):
        new_matches = []
        updated = False
        summoner = None
        message = None

        update_response = update_summoner(id)

        if not update_response['isError']:
            updated = True
            summoner = update_response['summoner']
            message = update_response['message']

            fetched_matches = fetch_match_list(summoner.summonerId)

            for match in fetched_matches:
                if Match.objects.filter(gameId=match['gameId']).count() == 0:
                    new_matches.append(match['gameId'])

        return UpdateSummoner(updated=updated, summoner=summoner, message=message, new_matches=new_matches)


class FetchMatchInput(graphene.InputObjectType):
    gameId = graphene.String()
    summonerId = graphene.String()


class FetchMatch(graphene.Mutation):
    class Arguments:
        input = FetchMatchInput()

    player = graphene.Field(PlayerType)

    @staticmethod
    def mutate(root, info, input):
        create_match(input.gameId)

        return FetchMatch(player=Player.objects.get(match__gameId=input.gameId, summoner__summonerId=input.summonerId))


class FetchAllRankedSummoners(graphene.Mutation):
    class Arguments:
        server = graphene.String()
        queue = graphene.String()

    Output = FunctionType

    @staticmethod
    def mutate(root, info, server, queue):
        get_all_ranked_summoners(server, queue)

        return FunctionType(success=True)


class ImprovementLogInput(graphene.InputObjectType):
    summonerId = graphene.String()
    gameId = graphene.Int()

    good = graphene.String()
    bad = graphene.String()
    opponent = graphene.List(graphene.String)
    lp = graphene.Int()


class UpdateImprovementLog(graphene.Mutation):
    class Arguments:
        input = ImprovementLogInput()

    result = graphene.String()

    @staticmethod
    def mutate(root, info, input):

        # Get the log object or create a new one.
        try:
            log = ImprovementLog.objects.get(summoner__summonerId=input.summonerId, match__gameId=input.gameId)

        except ImprovementLog.DoesNotExist:
            log = ImprovementLog.objects.create(
                summoner=Summoner.objects.get(summonerId=input.summonerId),
                match=Match.objects.get(gameId=input.gameId),
            )

        # Input the fields and save the log.
        log.good = input.good
        log.bad = input.bad
        log.lp = input.lp

        # Clear the opponents and re-add.
        log.opponent.clear()
        for champion in input.opponent:
            log.opponent.add(Champion.objects.get(champId=champion))

        log.save()

        return UpdateImprovementLog(result='Success!')


class RegisterInput(graphene.InputObjectType):
    username = graphene.String(required=True)
    email = graphene.String(required=True)
    password = graphene.String(required=True)
    key = graphene.String(required=True)


class Register(graphene.Mutation):
    class Arguments:
        input = RegisterInput()

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(root, info, input):

        try:
            access_key = AccessCode.objects.get(key=input.key)

            if access_key.used is False:

                try:

                    # Create the new user.
                    user = User.objects.create(
                        username=input.username,
                        email=input.email,
                        is_active=True
                    )
                    user.set_password(input.password)
                    user.save()

                    # Deactivate the Access Key used.
                    access_key.used = True
                    access_key.archived = True
                    access_key.user = user
                    access_key.date_used = datetime.now()
                    access_key.save()

                    # Send confirmation email.
                    mail_subject = 'Welcome to Ally! Let\'s activate your account.'
                    mail_plain = render_to_string('dashboard/email/email_confirmation.txt', {
                        'user': user,
                        'domain': 'ally.gg',
                        'username': user.username,
                        'token': account_activation_token.make_token(user),
                    })
                    mail_html = render_to_string('dashboard/email/email_confirmation.html', {
                        'user': user,
                        'domain': 'ally.gg',
                        'username': user.username,
                        'token': account_activation_token.make_token(user),
                    })

                    print('test')

                    send_mail(
                        mail_subject,  # Email subject.
                        mail_plain,  # Email plaintext.
                        'noreply@ally.gg',  # Email 'From' address.
                        [user.email, ],  # Email 'To' addresses. This must be a list or tuple.
                        html_message=mail_html,  # Email in HTML.
                    )

                    print('test2')

                    return Register(success=bool(user.id))

                except IntegrityError:
                    errors = ["email", "Email already registered."]
                    return Register(success=False, errors=errors)

            else:
                errors = ["key", "Access Key has already been used."]
                return Register(success=False, errors=errors)

        except AccessCode.DoesNotExist:
            errors = ["key", "Access Key does not exist."]
            return Register(success=False, errors=errors)


class CreateAccessKey(graphene.Mutation):
    key = graphene.String()

    @staticmethod
    def mutate(root, info):
        return CreateAccessKey(key=generate_access_code())


class Mutation(graphene.ObjectType):
    create_summoner = CreateSummoner.Field()
    update_summoner = UpdateSummoner.Field()
    fetch_match = FetchMatch.Field()
    fetch_all_ranked_summoners = FetchAllRankedSummoners.Field()
    update_improvement_log = UpdateImprovementLog.Field()
    register = Register.Field()
    create_access_key = CreateAccessKey.Field()
