from __future__ import absolute_import, unicode_literals
from celery.signals import celeryd_init
from dashboard.functions.general import *
from dashboard.functions.match import create_match
from dashboard.functions.game_data import *
from dynamic_preferences.registries import global_preferences_registry
from AllyGG.celery import app
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from AllyGG import schema


@celeryd_init.connect
def startup_tasks(sender=None, conf=None, **kwargs):
    # Clean out old queue
    app.control.purge()

    # Update the game data on startup.
    update_game_data(get_latest_version())
    print('Ally.GG is ready to go!')


@app.task
def task__update_summoner(summoner_id):
    update_summoner(summoner_id)

    room_group_name = 'summoner_%s' % summoner_id

    result = schema.schema.execute(
        '''
        {{
          summoner(summonerId: "{summoner_id}") {{
              summonerId
              summonerName
              profileIconId
              summonerLevel
              lastUpdated
              rankedSolo {{
                tier
                rank
                rankNumber
                lp
                leagueName
                wins
                losses
                ringValues
              }}
              rankedFlex5 {{
                tier
                rank
                rankNumber
                lp
                leagueName
                wins
                losses
                ringValues
              }}
              rankedFlex3 {{
                tier
                rank
                rankNumber
                lp
                leagueName
                wins
                losses
                ringValues
              }}
            }}
        }}
        '''.format(summoner_id=summoner_id)
    )

    async_to_sync(get_channel_layer().group_send)(
        room_group_name,
        {
            'type': 'celery',
            'message': 'Summoner Updated!',
            'data': {
                'summoner': json.dumps(result.data)
            }
        }
    )

    return True


@app.task
def task__fetch_match(game_id, summoner_id):
    create_match(game_id)

    room_group_name = 'summoner_%s' % summoner_id

    result = schema.schema.execute(
        '''
        {{
          player(summonerId: "{summoner_id}", gameId: {gameId}) {{
            match {{
              gameId
              queue
              gameDurationTime
              timeago
              timestamp
              players {{
                participantId
                team {{
                  teamId
                }}
                summoner {{
                  summonerName
                  rankedSolo {{
                    tier
                    rank
                    rankNumber
                    lp
                    leagueName
                    wins
                    losses
                    ringValues
                  }}
                  rankedFlex5 {{
                    tier
                    rank
                    rankNumber
                    lp
                    leagueName
                    wins
                    losses
                    ringValues
                  }}
                  rankedFlex3 {{
                    tier
                    rank
                    rankNumber
                    lp
                    leagueName
                    wins
                    losses
                    ringValues
                  }}
                }}
              }}
            }}
            champion {{
              key
              name
              champId
            }}
            lane
            laneOpponent {{
              champion {{
                key
                name
                champId
              }}
            }}
            win
            kills
            deaths
            assists
            kdaAverage
            champLevel
            killParticipation
            totalMinionsKilled
            csPmin
            item0 {{
              itemId
              name
            }}
            item1 {{
              itemId
              name
            }}
            item2 {{
              itemId
              name
            }}
            item3 {{
              itemId
              name
            }}
            item4 {{
              itemId
              name
            }}
            item5 {{
              itemId
              name
            }}
            item6 {{
              itemId
              name
            }}
            spell1Id {{
              name
              imageFull
            }}
            spell2Id {{
              name
              imageFull
            }}
            perk0 {{
              name
              icon
            }}
            perkSubStyle
            perk4 {{
              name
            }}
          }}
        }}
        '''.format(summoner_id=summoner_id, gameId=game_id)
    )

    async_to_sync(get_channel_layer().group_send)(
        room_group_name,
        {
            'type': 'celery',
            'message': 'New match added: ' + str(game_id),
            'data': {
                'match': json.dumps(result.data)
            }
        }
    )

    return True


@app.task
def task_update_version():
    # Get the Ally.GG global settings.
    global_preferences = global_preferences_registry.manager()

    # Fetch the latest version according to the Riot Static API.
    latest_version = get_latest_version()

    # Check that we're up to date, if we're not then update our settings.
    if latest_version != global_preferences['LATEST_PATCH']:
        global_preferences['LATEST_PATCH'] = latest_version


@app.task
def task_update_stats():
    # Get the Ally.GG global settings.
    global_preferences = global_preferences_registry.manager()

    # Update all stats.
    global_preferences['stats__UNRANKED_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier=None).exclude(date_updated=None).count()), 0)
    global_preferences['stats__IRON_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Iron').count()), 0)
    global_preferences['stats__BRONZE_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Bronze').count()), 0)
    global_preferences['stats__SILVER_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Silver').count()), 0)
    global_preferences['stats__GOLD_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Gold').count()), 0)
    global_preferences['stats__PLATINUM_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Platinum').count()), 0)
    global_preferences['stats__DIAMOND_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Diamond').count()), 0)
    global_preferences['stats__MASTER_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Master').count()), 0)
    global_preferences['stats__GRANDMASTER_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Grandmaster').count()), 0)
    global_preferences['stats__CHALLENGER_COUNT'] = "{:,}".format(
        int(Summoner.objects.filter(soloQ_tier__name='Challenger').count()), 0)
    global_preferences['stats__UPDATED_SUMMONER_COUNT'] = "{:,}".format(
        int(Summoner.objects.all().exclude(date_updated=None).count()), 0)
    global_preferences['stats__SUMMONER_COUNT'] = "{:,}".format(int(Summoner.objects.all().count()), 0)
    global_preferences['stats__MATCH_COUNT'] = "{:,}".format(int(Match.objects.all().count()), 0)
