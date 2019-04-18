from dashboard.functions.general import *
from dashboard.models import *
from django.db.models import Sum

def global_context(request):
    # User Information
    isProfile = Profile.objects.all().filter(user=request.user) if request.user.is_authenticated == True else None
    profile = Profile.objects.get(user=request.user) if isProfile else None
    globalSettings = Setting.objects.get(name='Global') if Setting.objects.filter(name='Global').count() == 1 else Setting.objects.create(name='Global', latestVersion=get_latest_version())
    total_kills = Player.objects.aggregate(Sum('kills'))

    return {
    'DEBUG': settings.DEBUG,
    'GSETTINGS': globalSettings,
    'SUMMONER_COUNT': "{:,}".format(int(Summoner.objects.all().count()), 0),
    'TOTAL_KILLS': "{:,}".format(int(total_kills['kills__sum']), 0),
    'MATCH_COUNT': "{:,}".format(int(Match.objects.all().count()), 0),
    'MY_PROFILE': profile,
    'MY_SUMMONERS': Summoner.objects.filter(user_profile=profile) if isProfile else None,
    'CURRENT_PATCH': globalSettings.latestVersion,
    }
