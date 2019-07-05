from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('summoner/<server>/<summonerId>', consumers.SummonerConsumer),
    path('dashboard/<userId>', consumers.UserConsumer),
    path('admin', consumers.AdminConsumer)
]
