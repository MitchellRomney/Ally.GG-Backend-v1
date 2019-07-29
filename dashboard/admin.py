from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from dashboard.models import *


# Inlines


class PlayerInline(admin.TabularInline):
    model = Player

    list_display = (
        'summonerName',
    )


class SummonerInline(admin.TabularInline):
    model = Summoner

    fields = [
        'summonerName',
        'summonerId'
    ]

    extra = 0

# Main Object Admins


class SummonerAdmin(admin.ModelAdmin):
    model = Summoner

    list_display = (
        'summonerName',
        'user_profile',
        'server',
        'summonerLevel',
        'soloQ_tier',
        'flexTT_tier',
        'flexSR_tier',
        'date_created',
        'date_updated'
    )

    list_select_related = (
        'user_profile',
        'soloQ_tier',
        'flexTT_tier',
        'flexSR_tier',
    )

    search_fields = (
        'summonerName',
        'summonerId',
        'user_profile__user__username',
        'soloQ_tier__name'
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        readonly_fields.remove('user_profile')
        return readonly_fields


class ProfileAdmin(admin.ModelAdmin):
    model = Profile

    list_display = (
        'user',
        'premium',
        'dark_mode',
        'email',
        'email_confirmed',
        'date_created',
        'date_modified'
    )

    list_select_related = (
        'user',
    )

    readonly_fields = (
        'date_created',
        'date_modified'
    )

    search_fields = (
        'user',
    )

    @staticmethod
    def email(self):
        return self.user.email


class TeamAdmin(admin.ModelAdmin):
    model = Team


class PlayerAdmin(admin.ModelAdmin):
    model = Player

    list_display = (
        'summoner',
        'champion',
        'date_created',
    )

    list_select_related = (
        'summoner',
        'champion',
        'match',
    )

    search_fields = (
        'match__gameId',
        'summoner__summonerName'
    )

    list_per_page = 50

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields


class MatchAdmin(admin.ModelAdmin):
    model = Match

    list_display = (
        'platformId',
        'gameId',
        'queueId',
        'seasonId',
        'mapId',
        'date_created'
    )

    search_fields = (
        'gameId',
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(set(
            [field.name for field in self.opts.local_fields] +
            [field.name for field in self.opts.local_many_to_many]
        ))
        return readonly_fields


class ChampionAdmin(admin.ModelAdmin):
    model = Champion

    list_display = (
        'name',
        'key',
        'version'
    )

    search_fields = (
        'name',
    )


class ChatRoomAdmin(admin.ModelAdmin):
    model = ChatRoom

    list_display = (
        'roomId',
        'date_created',
        'date_updated',
    )


class RuneAdmin(admin.ModelAdmin):
    model = Rune

    list_display = (
        'runeId',
        'name',
        'version',
    )


class ItemAdmin(admin.ModelAdmin):
    model = Item

    list_display = (
        'name',
        'version'
    )


class SummonerSpellAdmin(admin.ModelAdmin):
    model = SummonerSpell

    list_display = (
        'name',
        'version'
    )


class RankedTierAdmin(admin.ModelAdmin):
    model = RankedTier

    list_display = (
        'key',
        'name',
        'order'
    )


class AccessCodeAdmin(admin.ModelAdmin):
    model = AccessCode

    list_display = (
        'key',
        'used',
        'user',
        'date_used',
        'date_created',
        'archived'
    )


class ImprovementLogAdmin(admin.ModelAdmin):
    model = ImprovementLog

    list_display = (
        'summoner',
        'match',

        'archived',
        'date_modified',
        'date_created',
    )

    list_select_related = (
        'summoner',
        'match',
    )

    readonly_fields = (
        'summoner',
        'match',
        'date_modified',
        'date_created',
    )


class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'email',
        'last_login',
        'date_joined',
    )


class ThirdPartyVerificationAdmin(admin.ModelAdmin):
    model = ThirdPartyVerification

    list_display = (
        'user',
        'summoner',
        'verified',
        'date_modified',
        'date_created',
    )

    list_select_related = (
        'user',
        'summoner',
    )

    readonly_fields = (
        'summoner',
        'user',
        'date_modified',
        'date_created',
    )


admin.site.unregister(Group)
admin.site.unregister(User)

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Summoner, SummonerAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Champion, ChampionAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Rune, RuneAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(SummonerSpell, SummonerSpellAdmin)
admin.site.register(RankedTier, RankedTierAdmin)
admin.site.register(AccessCode, AccessCodeAdmin)
admin.site.register(ImprovementLog, ImprovementLogAdmin)
admin.site.register(ThirdPartyVerification, ThirdPartyVerificationAdmin)
