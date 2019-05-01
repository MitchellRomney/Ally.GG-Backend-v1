from __future__ import absolute_import, unicode_literals
from celery import task
from celery.signals import celeryd_init
from dashboard.functions.general import *
from dashboard.functions.match import *
from dashboard.functions.game_data import *
from dynamic_preferences.registries import global_preferences_registry
from django.db.models import Sum
import time


@celeryd_init.connect
def startup_tasks(sender=None, conf=None, **kwargs):
    # Update the game data on startup.
    update_game_data(get_latest_version())
    print('Ally.GG is ready to go!')


@task
def task_update_summoners():

    # Get the oldest Summoner in the database who has never been updated.
    summoner = Summoner.objects.filter(date_updated=None).order_by('date_created')[:1].get()

    # Update the Summoner
    try:
        update_summoner(summoner.summonerId)
    except TypeError as type_error:  # TypeError is the Riot API encountered an error. Wait 1 second and try again.
        print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + str(type_error))
        time.sleep(1)
        try:
            update_summoner(summoner.summonerId)
        except TypeError:  # If the Riot API is still being difficult, skip this update.
            return None

    # Grab the latest 10 matches from the Summoner.
    latest_matches = fetch_match_list(summoner.summonerId)

    # Check if the Riot API failed, if it did then try again. If it still fails, stop the update.
    if latest_matches is None:
        latest_matches = fetch_match_list(summoner.summonerId)
        if latest_matches is None:
            return None

    # For each of the matches in the match list, if they don't exist add them to the database.
    for match in latest_matches:
        if Match.objects.filter(gameId=match['gameId']).count() == 0:

            try:
                create_match(match['gameId'])
            except KeyError:  # TypeError is the Riot API encountered an error. Wait 1 second and try again.
                time.sleep(1)
                try:
                    create_match(match['gameId'])
                except KeyError:  # If the Riot API is still being difficult, skip this update.
                    return None

    return None

@task
def task_update_version():
    # Get the Ally.GG global settings.
    global_preferences = global_preferences_registry.manager()

    # Fetch the latest version according to the Riot Static API.
    latest_version = get_latest_version()

    # Check that we're up to date, if we're not then update our settings.
    if latest_version != global_preferences['LATEST_PATCH']:
        global_preferences['LATEST_PATCH'] = latest_version

@task
def task_update_stats():
    # Calculate the total sum of all Kills from all players in the database.
    total_kills = Player.objects.aggregate(Sum('kills'))

    # Get the Ally.GG global settings.
    global_preferences = global_preferences_registry.manager()

    # Update all stats.
    global_preferences['stats__UNRANKED_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier=None).exclude(date_updated=None).count()), 0)
    global_preferences['stats__IRON_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Iron').count()), 0)
    global_preferences['stats__BRONZE_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Bronze').count()), 0)
    global_preferences['stats__SILVER_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Silver').count()), 0)
    global_preferences['stats__GOLD_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Gold').count()), 0)
    global_preferences['stats__PLATINUM_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Platinum').count()), 0)
    global_preferences['stats__DIAMOND_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Diamond').count()), 0)
    global_preferences['stats__MASTER_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Master').count()), 0)
    global_preferences['stats__GRANDMASTER_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Grandmaster').count()), 0)
    global_preferences['stats__CHALLENGER_COUNT'] = "{:,}".format(int(Summoner.objects.filter(soloQ_tier__name='Challenger').count()), 0)
    global_preferences['stats__UPDATED_SUMMONER_COUNT'] = "{:,}".format(int(Summoner.objects.all().exclude(date_updated=None).count()), 0)
    global_preferences['stats__SUMMONER_COUNT'] = "{:,}".format(int(Summoner.objects.all().count()), 0)
    global_preferences['stats__MATCH_COUNT'] = "{:,}".format(int(Match.objects.all().count()), 0)
    global_preferences['stats__TOTAL_KILLS'] = "{:,}".format(int(total_kills['kills__sum']), 0) if total_kills['kills__sum'] else 0
