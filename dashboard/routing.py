from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('summoner/<summonerName>', consumers.SummonerConsumer),
    path('dashboard/<userId>', consumers.UserConsumer)
]
