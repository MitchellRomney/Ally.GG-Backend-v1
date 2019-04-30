from dashboard.models import *
from dynamic_preferences.registries import global_preferences_registry
from django.conf import settings


def global_context(request):
    # User Information
    is_profile = Profile.objects.all().filter(user=request.user) if request.user.is_authenticated is True else None
    profile = Profile.objects.get(user=request.user) if is_profile else None

    return {
        'DEBUG': settings.DEBUG,
        'MY_PROFILE': profile,
        'MY_SUMMONERS': Summoner.objects.filter(user_profile=profile) if profile else None,
        'SETTINGS': global_preferences_registry.manager()
    }
