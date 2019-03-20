from django.contrib import admin
from django.contrib.auth.models import Group
from dashboard.models import Summoner, Match, Match_Team, Match_Player

class SummonerAdmin(admin.ModelAdmin):
    model = Summoner
    list_display = ('summonerName',)
    readonly_fields = ('summonerId', 'accountId', 'puuid',)

class TeamAdmin(admin.ModelAdmin):
    model = Match_Team

class TeamInline(admin.TabularInline):
    model = Match_Team

class PlayerAdmin(admin.ModelAdmin):
    model = Match_Player

class PlayerInline(admin.TabularInline):
    model = Match_Player

class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = ('platformId', 'gameId', 'queueId', 'seasonId', 'mapId', 'date_created')

    inlines = [
        TeamInline,
        PlayerInline
        ]


admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Match_Team, TeamAdmin)
admin.site.register(Match_Player, PlayerAdmin)
admin.site.unregister(Group)
