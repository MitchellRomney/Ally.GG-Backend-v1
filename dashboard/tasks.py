from __future__ import absolute_import, unicode_literals
from celery import task
from dashboard.functions.general import *
from dashboard.functions.game_data import *
from django.shortcuts import get_object_or_404

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
            fetch_match(match['gameId'])
            new_match = Match.objects.filter(gameId=match['gameId'])[:1].get()
            if new_match:
                check_match_integrity(new_match)

    return None

@task
def task_update_version():
    global_settings = Setting.objects.get(name='Global') if Setting.objects.filter(name='Global').count() == 1 else None
    if global_settings:
        latest_version = get_latest_version()
        if latest_version != global_settings.latestVersion:
            global_settings.latestVersion = latest_version
            global_settings.save()
            print(Fore.GREEN + 'New Version: ' + Style.RESET_ALL + latest_version)
        else:
            print(Fore.YELLOW + 'Current Version up to date.')
    else:
        global_settings = Setting.objects.create(name='Global', latestVersion=get_latest_version())
        print(Fore.GREEN + 'New Version: ' + Style.RESET_ALL + global_settings.latestVersion)
