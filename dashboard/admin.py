from django.contrib import admin
from django.contrib.auth.models import Group
from dashboard.models import *

class TeamInline(admin.TabularInline):
    model = Team

class PlayerInline(admin.TabularInline):
    model = Player
    list_display = ('summonerName',)

class SummonerInline(admin.TabularInline):
    model = Summoner
    fields = ['summonerName', 'summonerId']
    extra = 0

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

class SettingAdmin(admin.ModelAdmin):
    model = Setting
    list_display = ('name',)

class ChatRoomAdmin(admin.ModelAdmin):
    model = ChatRoom
    list_display = ('roomId', 'date_created', 'date_updated',)

class RuneAdmin(admin.ModelAdmin):
    model = Rune
    list_display = ('name','version')

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('name', 'version')

class SummonerSpellAdmin(admin.ModelAdmin):
    model = SummonerSpell
    list_display = ('name', 'version')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Champion, ChampionAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Rune, RuneAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SummonerSpell, SummonerSpellAdmin)
admin.site.unregister(Group)
