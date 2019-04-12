from __future__ import absolute_import, unicode_literals
from celery import task
from dashboard.functions.general import *
from django.shortcuts import get_object_or_404

@task
def task_updateSummoners():
    summoner = Summoner.objects.filter(date_updated=None).order_by('date_created')[:1].get()

    update_summoner(summoner.puuid)

    latestMatches = fetch_match_list(summoner.puuid)

    if 'isError' in latestMatches:
        if latestMatches['isError']:
            return None

    for match in latestMatches:
        existingMatch = Match.objects.filter(gameId=match['gameId'])
        if existingMatch.count() == 0:
            fetch = fetch_match(match['gameId'])

            queryset = Match.objects.filter(gameId=match['gameId'])
            newMatch = get_object_or_404(queryset, gameId=match['gameId'])

            if newMatch:
                matchClean = check_match_integrity(newMatch)

    return None

@task
def task_updateVersion():
    globalSettings = Setting.objects.get(name='Global') if Setting.objects.filter(name='Global').count() == 1 else None
    if globalSettings:
        latestVersion = get_latest_version()
        if latestVersion != globalSettings.latestVersion:
            globalSettings.latestVersion = latestVersion
            globalSettings.save()
            print(Fore.GREEN + 'New Version: ' + Style.RESET_ALL + latestVersion)
        else:
            print(Fore.YELLOW + 'Current Version up to date.')
    else:
        globalSettings = Setting.objects.create(name='Global', latestVersion=get_latest_version())
        print(Fore.GREEN + 'New Version: ' + Style.RESET_ALL + globalSettings.latestVersion)
