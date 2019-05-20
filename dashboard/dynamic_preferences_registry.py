from dynamic_preferences.types import StringPreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry

stats = Section('stats')


@global_preferences_registry.register
class LatestPatch(StringPreference):
    name = 'LATEST_PATCH'
    default = '9.0.0'


@global_preferences_registry.register
class SummonerCount(StringPreference):
    name = 'SUMMONER_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class UpdatedSummonerCount(StringPreference):
    name = 'UPDATED_SUMMONER_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class MatchCount(StringPreference):
    name = 'MATCH_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class TotalKills(StringPreference):
    name = 'TOTAL_KILLS'
    default = '0'
    section = stats


@global_preferences_registry.register
class UnrankedCount(StringPreference):
    name = 'UNRANKED_COUNT'
    default = '0'
    section = stats

@global_preferences_registry.register
class IronCount(StringPreference):
    name = 'IRON_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class BronzeCount(StringPreference):
    name = 'BRONZE_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class SilverCount(StringPreference):
    name = 'SILVER_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class GoldCount(StringPreference):
    name = 'GOLD_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class PlatinumCount(StringPreference):
    name = 'PLATINUM_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class DiamondCount(StringPreference):
    name = 'DIAMOND_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class MasterCount(StringPreference):
    name = 'MASTER_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class GrandmasterCount(StringPreference):
    name = 'GRANDMASTER_COUNT'
    default = '0'
    section = stats


@global_preferences_registry.register
class ChallengerCount(StringPreference):
    name = 'CHALLENGER_COUNT'
    default = '0'
    section = stats
