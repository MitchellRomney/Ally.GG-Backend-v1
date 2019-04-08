from __future__ import absolute_import, unicode_literals
from celery import task
from dashboard.functions.summoners import *
from dashboard.functions.general import *
from django.shortcuts import get_object_or_404

@task()
def task_updateSummoners():
    summoner = Summoner.objects.filter(date_updated=None).order_by('date_created')[:1].get()

    updateSummoner(summoner.puuid)

    latestMatches = fetchMatchList(summoner.puuid)

    if 'isError' in latestMatches:
        if latestMatches['isError']:
            return None

    for match in latestMatches:
        existingMatch = Match.objects.filter(gameId=match['gameId'])
        if existingMatch.count() == 0:
            fetch = fetchMatch(match['gameId'])

            queryset = Match.objects.filter(gameId=match['gameId'])
            newMatch = get_object_or_404(queryset, gameId=match['gameId'])

            if newMatch:
                matchClean = checkMatchIntegrity(newMatch)

    return None

@task()
def task_updateVersion():
    globalSettings = Setting.objects.get(name='Global') if Setting.objects.filter(name='Global').count() == 1 else None
    if globalSettings:
        latestVersion = getLatestVersion()
        if latestVersion != globalSettings.latestVersion:
            globalSettings.latestVersion = latestVersion
            globalSettings.save()
            print(Fore.GREEN + 'New Version: ' + Style.RESET_ALL + latestVersion)
        else:
            print(Fore.YELLOW + 'Current Version up to date.')
    else:
        globalSettings = Setting.objects.create(name='Global',latestVersion=getLatestVersion())
        print(Fore.GREEN + 'New Version: ' + Style.RESET_ALL + globalSettings.latestVersion)
