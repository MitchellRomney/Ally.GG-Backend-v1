from dashboard.functions.general import *
from dashboard.models import *
from dynamic_preferences.registries import global_preferences_registry


def global_context(request):
    # User Information
    isProfile = Profile.objects.all().filter(user=request.user) if request.user.is_authenticated == True else None
    profile = Profile.objects.get(user=request.user) if isProfile else None

    return {
        'DEBUG': settings.DEBUG,
        'MY_PROFILE': profile,
        'MY_SUMMONERS': Summoner.objects.filter(user_profile=profile) if isProfile else None,
        'SETTINGS': global_preferences_registry.manager()
    }
