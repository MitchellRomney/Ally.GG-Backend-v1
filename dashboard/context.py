from django.conf import settings
from dashboard.models import *

def global_context(request):
    # User Information
    isProfile = Profile.objects.all().filter(user=request.user) if request.user.is_authenticated == True else None
    profile = Profile.objects.get(user=request.user) if isProfile else None

    return {
    'DEBUG': settings.DEBUG,
    'GSETTINGS': Setting.objects.get(name='Global') if Setting.objects.filter(name='Global').count() == 1 else None,
    'SUMMONER_COUNT': Summoner.objects.all().count(),
    'MATCH_COUNT': Match.objects.all().count(),
    'PROFILE': profile,
    'MY_SUMMONERS': Summoner.objects.filter(user_profile=profile) if isProfile else None,
    }
