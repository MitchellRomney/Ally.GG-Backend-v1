from dashboard.functions.general import *
from dashboard.models import *

def global_context(request):
    # User Information
    isProfile = Profile.objects.all().filter(user=request.user) if request.user.is_authenticated == True else None
    profile = Profile.objects.get(user=request.user) if isProfile else None
    globalSettings = Setting.objects.get(name='Global') if Setting.objects.filter(name='Global').count() == 1 else Setting.objects.create(name='Global', latestVersion=get_latest_version())

    return {
    'DEBUG': settings.DEBUG,
    'GSETTINGS': globalSettings,
    'SUMMONER_COUNT': Summoner.objects.all().count(),
    'MATCH_COUNT': Match.objects.all().count(),
    'MY_PROFILE': profile,
    'MY_SUMMONERS': Summoner.objects.filter(user_profile=profile) if isProfile else None,
    'CURRENT_PATCH': globalSettings.latestVersion,
    }
