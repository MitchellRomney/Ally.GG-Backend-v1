from django.contrib import admin
from django.contrib.auth.models import Group, User
from dashboard.models import *

class TeamInline(admin.TabularInline):
    model = Team

class PlayerInline(admin.TabularInline):
    model = Player
    list_display = ('summonerName',)

class SummonerInline(admin.TabularInline):
    model = Summoner
    readonly_fields = ('summonerId', 'accountId', 'puuid', 'date_updated')

class MatchInline(admin.TabularInline):
    model = Match.players.through

class SummonerAdmin(admin.ModelAdmin):
    model = Summoner
    list_display = ('summonerName', 'date_created', 'date_updated')
    readonly_fields = ('summonerId', 'accountId', 'puuid', 'date_created', 'date_updated')
    inlines = [
        MatchInline
    ]
    search_fields = ('summonerName',)

class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'first_name', 'last_name', 'email', 'date_created', 'date_modified')
    readonly_fields = ('date_created', 'date_modified')
    inlines = [
        SummonerInline
        ]
    search_fields = ('user',)

class TeamAdmin(admin.ModelAdmin):
    model = Team

class PlayerAdmin(admin.ModelAdmin):
    model = Player

    search_fields = ('match__gameId', 'summoner__summonerName')

class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = ('platformId', 'gameId', 'queueId', 'seasonId', 'mapId', 'date_created')

    inlines = [
        TeamInline,
        ]

    search_fields = ('gameId',)

class ChampionAdmin(admin.ModelAdmin):
    model = Champion
    list_display = ('name', 'key', 'version')
    search_fields = ('name',)

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Champion, ChampionAdmin)
admin.site.unregister(Group)
