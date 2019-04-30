from __future__ import absolute_import, unicode_literals
from celery import task
from dashboard.functions.general import *
from dashboard.functions.match import *
from dashboard.functions.game_data import *
from dynamic_preferences.registries import global_preferences_registry
from django.db.models import Sum


@task
def task_update_summoners():
    champions = Champion.objects.all()
    runes = Rune.objects.all()
    summoner_spells = SummonerSpell.objects.all()
    items = Item.objects.all()
    ranked_tiers = RankedTier.objects.all()
    if champions.count() == 0 or runes.count() == 0 or summoner_spells.count() == 0 or items.count() == 0 \
            or ranked_tiers.count() == 0:
        update_game_data(get_latest_version())

    summoner = Summoner.objects.filter(date_updated=None).order_by('date_created')[:1].get()
    update_summoner(summoner.summonerId)
    latest_matches = fetch_match_list(summoner.summonerId)

    for match in latest_matches:
        if Match.objects.filter(gameId=match['gameId']).count() == 0:
            create_match(match['gameId'])

    return None

@task
def task_update_version():
    global_preferences = global_preferences_registry.manager()
    latest_version = get_latest_version()
    if latest_version != global_preferences['LATEST_PATCH']:
        global_preferences['LATEST_PATCH'] = latest_version
        print(Fore.GREEN + 'New Version: ' + Style.RESET_ALL + latest_version)
    else:
        print(Fore.YELLOW + 'Current Version up to date.')

@task
def task_update_stats():
    total_kills = Player.objects.aggregate(Sum('kills'))

    global_preferences = global_preferences_registry.manager()
    global_preferences['stats__UNRANKED_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier=None).count()), 0)
    global_preferences['stats__IRON_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Iron').count()), 0)
    global_preferences['stats__BRONZE_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Bronze').count()), 0)
    global_preferences['stats__SILVER_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Silver').count()), 0)
    global_preferences['stats__GOLD_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Gold').count()), 0)
    global_preferences['stats__PLATINUM_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Platinum').count()), 0)
    global_preferences['stats__DIAMOND_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Diamond').count()), 0)
    global_preferences['stats__MASTER_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Master').count()), 0)
    global_preferences['stats__GRANDMASTER_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Grandmaster').count()), 0)
    global_preferences['stats__CHALLENGER_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Challenger').count()), 0)
    global_preferences['stats__SUMMONER_COUNT'] = "{:,}".format(int(Summoner.objects.all().count()), 0)
    global_preferences['stats__MATCH_COUNT'] = "{:,}".format(int(Match.objects.all().count()), 0)
    global_preferences['stats__TOTAL_KILLS'] = "{:,}".format(int(total_kills['kills__sum']), 0) if total_kills['kills__sum'] else 0
