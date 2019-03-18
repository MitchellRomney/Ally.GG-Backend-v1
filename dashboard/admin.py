from django.contrib import admin
from django.contrib.auth.models import Group
from dashboard.models import Summoner

class SummonerAdmin(admin.ModelAdmin):
    model = Summoner
    list_display = ('summonerName',)
    readonly_fields = ('summonerId', 'accountId', 'puuid',)

admin.site.register(Summoner, SummonerAdmin)
admin.site.unregister(Group)
