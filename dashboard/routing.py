from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('summoner/<summonerId>', consumers.SummonerConsumer),
    path('dashboard/<userId>', consumers.UserConsumer)
]
