from dashboard.functions.api import *
from dashboard.models import *
from django.utils import timezone
from django.db import IntegrityError
from colorama import Fore, Style


def add_summoner(method, value):

    # Fetch Summoner information from the Riot API.
    summoner_info = fetch_riot_api('OC1', 'summoner', 'v4', 'summoners/' + value) \
        if method == 'SummonerId' else fetch_riot_api('OC1', 'summoner', 'v4', 'summoners/by-name/' + value)

    if 'isError' in summoner_info:
        if summoner_info['isError'] and not summoner_info['ignore']:
            return {
                'isError': True,
                'message': summoner_info['message'],
                'summonerId': None,
                'summoner': None
            }

    # Search if Summoner already exists in database.
    existing_summoner = Summoner.objects.filter(summonerId=summoner_info['id'])

    # If Summoner doesn't exist, create it.
    if existing_summoner.count() == 0:
        try:
            new_summoner = Summoner.objects.create(
                # Ids
                summonerName=summoner_info['name'],
                summonerId=summoner_info['id'],
                puuid=summoner_info['puuid'],
                accountId=summoner_info['accountId'],

                # General
                server='OC1',
                profileIconId=summoner_info['profileIconId'],
                summonerLevel=summoner_info['summonerLevel'],

                # System
                date_created=timezone.now(),
            )

        except IntegrityError:  # This shouldn't happen, but just in case.

            # Get the existing Summoner that caused the IntegrityError.
            existing_summoner = Summoner.objects.get(summonerId=summoner_info['id'])
            return {
                'isError': True,
                'message': 'Summoner already exists.',
                'summonerId': existing_summoner.summonerId,
                'summoner': existing_summoner
            }

        # Return success response.
        return {
            'isError': False,
            'message': 'New Summoner created!',
            'summonerId': new_summoner.summonerId,
            'summoner': new_summoner
        }

    # If someone is trying to add a Summoner that already exists, return error response.
    existing_summoner = Summoner.objects.get(summonerId=summoner_info['id'])
    return {
        'isError': True,
        'message': 'Summoner already exists.',
        'summonerId': existing_summoner.summonerId,
        'summoner': existing_summoner
    }


def update_summoner(summoner_id):

    # Get the Summoner you're trying to update.
    summoner = Summoner.objects.get(summonerId=summoner_id)

    # Set the date_updated field to now.
    summoner.date_updated = timezone.now()

    # Save the Summoner. This all happens immediately so the update summoner script doesn't pick it up twice.
    summoner.save()

    # Print to console that we're updating the Summoner.
    print(Fore.YELLOW + 'Updating Summoner: ' + Style.RESET_ALL + summoner.summonerName)

    # Fetch the Summoner information from the Riot API.
    summoner_info = fetch_riot_api('OC1', 'summoner', 'v4', 'summoners/' + summoner_id)

    # Update basic Summoner information.
    summoner.summonerName = summoner_info['name']
    summoner.profileIconId = summoner_info['profileIconId']
    summoner.summonerLevel = summoner_info['summonerLevel']

    # Fetch the Summoner Ranked information from the Riot API.
    ranked_info = fetch_riot_api('OC1', 'league', 'v4', 'entries/by-summoner/' + summoner.summonerId)

    # Iterate through the different Ranked Queues.
    for queue in ranked_info:

        # If the Summoner is ranked in SoloQ, update the SoloQ information.
        if queue['queueType'] == 'RANKED_SOLO_5x5':
            summoner.soloQ_leagueId = queue['leagueId']
            summoner.soloQ_tier = RankedTier.objects.get(key=queue['tier'])
            summoner.soloQ_hotStreak = queue['hotStreak']
            summoner.soloQ_wins = queue['wins']
            summoner.soloQ_losses = queue['losses']
            summoner.soloQ_veteran = queue['veteran']
            summoner.soloQ_rank = queue['rank']
            summoner.soloQ_inactive = queue['inactive']
            summoner.soloQ_freshBlood = queue['freshBlood']
            summoner.soloQ_leaguePoints = queue['leaguePoints']

        # If the Summoner is ranked in FlexQ, update the FlexQ information.
        elif queue['queueType'] == 'RANKED_FLEX_SR':
            summoner.flexSR_leagueId = queue['leagueId']
            summoner.flexSR_tier = RankedTier.objects.get(key=queue['tier'])
            summoner.flexSR_hotStreak = queue['hotStreak']
            summoner.flexSR_wins = queue['wins']
            summoner.flexSR_losses = queue['losses']
            summoner.flexSR_veteran = queue['veteran']
            summoner.flexSR_rank = queue['rank']
            summoner.flexSR_inactive = queue['inactive']
            summoner.flexSR_freshBlood = queue['freshBlood']
            summoner.flexSR_leaguePoints = queue['leaguePoints']

        # If the Summoner is ranked in 3v3, update the 3v3 information.
        elif queue['queueType'] == 'RANKED_FLEX_TT':
            summoner.flexTT_leagueId = queue['leagueId']
            summoner.flexTT_tier = RankedTier.objects.get(key=queue['tier'])
            summoner.flexTT_hotStreak = queue['hotStreak']
            summoner.flexTT_wins = queue['wins']
            summoner.flexTT_losses = queue['losses']
            summoner.flexTT_veteran = queue['veteran']
            summoner.flexTT_rank = queue['rank']
            summoner.flexTT_inactive = queue['inactive']
            summoner.flexTT_freshBlood = queue['freshBlood']
            summoner.flexTT_leaguePoints = queue['leaguePoints']

    # Save the newly updated Summoner.
    summoner.save()

    # Return a successful response.
    return {
        'message': 'Summoner Updated!',
        'summonerId': summoner.summonerId,
        'summoner': summoner,
        'isError': False
    }


def get_top_ranked(server, queue, tier):
    response = fetch_riot_api(server, 'league', 'v4', tier + 'leagues/by-queue/' + queue)

    count = 0

    for summoner in response['entries']:
        count += 1

        try:
            summoner_obj = Summoner.objects.get(summonerId=summoner['summonerId'])

            summoner_obj.summonerName = summoner['summonerName']

        except Summoner.DoesNotExist:
            # Fetch the Summoner information from the Riot API.
            summoner_info = fetch_riot_api('OC1', 'summoner', 'v4', 'summoners/' + summoner['summonerId'])

            summoner_obj = Summoner.objects.create(
                # Ids
                summonerName=summoner_info['name'],
                summonerId=summoner_info['id'],
                puuid=summoner_info['puuid'],
                accountId=summoner_info['accountId'],

                # General
                server=server,
                profileIconId=summoner_info['profileIconId'],
                summonerLevel=summoner_info['summonerLevel'],
            )

        if queue == 'RANKED_SOLO_5x5':
            summoner_obj.soloQ_leagueId = response['leagueId']
            summoner_obj.soloQ_leagueName = response['name']
            summoner_obj.soloQ_tier = RankedTier.objects.get(key=response['tier'])
            summoner_obj.soloQ_hotStreak = summoner['hotStreak']
            summoner_obj.soloQ_wins = summoner['wins']
            summoner_obj.soloQ_losses = summoner['losses']
            summoner_obj.soloQ_veteran = summoner['veteran']
            summoner_obj.soloQ_rank = summoner['rank']
            summoner_obj.soloQ_inactive = summoner['inactive']
            summoner_obj.soloQ_freshBlood = summoner['freshBlood']
            summoner_obj.soloQ_leaguePoints = summoner['leaguePoints']

        elif queue == 'RANKED_FLEX_SR':
            summoner_obj.flexSR_leagueId = response['id']
            summoner_obj.flexSR_leagueName = response['name']
            summoner_obj.flexSR_tier = RankedTier.objects.get(key=response['tier'])
            summoner_obj.flexSR_hotStreak = summoner['hotStreak']
            summoner_obj.flexSR_wins = summoner['wins']
            summoner_obj.flexSR_losses = summoner['losses']
            summoner_obj.flexSR_veteran = summoner['veteran']
            summoner_obj.flexSR_rank = summoner['rank']
            summoner_obj.flexSR_inactive = summoner['inactive']
            summoner_obj.flexSR_freshBlood = summoner['freshBlood']
            summoner_obj.flexSR_leaguePoints = summoner['leaguePoints']

        elif queue == 'RANKED_FLEX_TT':
            summoner_obj.flexTT_leagueId = response['id']
            summoner_obj.flexTT_leagueName = response['name']
            summoner_obj.flexTT_tier = RankedTier.objects.get(key=response['tier'])
            summoner_obj.flexTT_hotStreak = summoner['hotStreak']
            summoner_obj.flexTT_wins = summoner['wins']
            summoner_obj.flexTT_losses = summoner['losses']
            summoner_obj.flexTT_veteran = summoner['veteran']
            summoner_obj.flexTT_rank = summoner['rank']
            summoner_obj.flexTT_inactive = summoner['inactive']
            summoner_obj.flexTT_freshBlood = summoner['freshBlood']
            summoner_obj.flexTT_leaguePoints = summoner['leaguePoints']

        summoner_obj.save()

    print(Fore.YELLOW + str(count) + Style.RESET_ALL + ' Summoners in ' + tier + ' ' + queue + ' updated.')


def get_ranked(server, queue, tier):
    page = 1
    continue_next = True
    division = 'I'

    while continue_next:
        response = fetch_riot_api(server, 'league', 'v4', 'entries/' + queue + '/' + tier + '/' + division + '?page=' + str(page))

        count = 0

        for summoner in response:
            count += 1

            try:
                summoner_obj = Summoner.objects.get(summonerId=summoner['summonerId'])

                summoner_obj.summonerName = summoner['summonerName']

            except Summoner.DoesNotExist:
                # Fetch the Summoner information from the Riot API.
                summoner_info = fetch_riot_api('OC1', 'summoner', 'v4', 'summoners/' + summoner['summonerId'])

                summoner_obj = Summoner.objects.create(
                    # Ids
                    summonerName=summoner_info['name'],
                    summonerId=summoner_info['id'],
                    puuid=summoner_info['puuid'],
                    accountId=summoner_info['accountId'],

                    # General
                    server=server,
                    profileIconId=summoner_info['profileIconId'],
                    summonerLevel=summoner_info['summonerLevel'],
                )

            if queue == 'RANKED_SOLO_5x5':
                summoner_obj.soloQ_leagueId = summoner['leagueId']
                summoner_obj.soloQ_tier = RankedTier.objects.get(key=summoner['tier'])
                summoner_obj.soloQ_hotStreak = summoner['hotStreak']
                summoner_obj.soloQ_wins = summoner['wins']
                summoner_obj.soloQ_losses = summoner['losses']
                summoner_obj.soloQ_veteran = summoner['veteran']
                summoner_obj.soloQ_rank = summoner['rank']
                summoner_obj.soloQ_inactive = summoner['inactive']
                summoner_obj.soloQ_freshBlood = summoner['freshBlood']
                summoner_obj.soloQ_leaguePoints = summoner['leaguePoints']

            elif queue == 'RANKED_FLEX_SR':
                summoner_obj.flexSR_leagueId = response['id']
                summoner_obj.flexSR_tier = RankedTier.objects.get(key=response['tier'])
                summoner_obj.flexSR_hotStreak = summoner['hotStreak']
                summoner_obj.flexSR_wins = summoner['wins']
                summoner_obj.flexSR_losses = summoner['losses']
                summoner_obj.flexSR_veteran = summoner['veteran']
                summoner_obj.flexSR_rank = summoner['rank']
                summoner_obj.flexSR_inactive = summoner['inactive']
                summoner_obj.flexSR_freshBlood = summoner['freshBlood']
                summoner_obj.flexSR_leaguePoints = summoner['leaguePoints']

            elif queue == 'RANKED_FLEX_TT':
                summoner_obj.flexTT_leagueId = response['id']
                summoner_obj.flexTT_tier = RankedTier.objects.get(key=response['tier'])
                summoner_obj.flexTT_hotStreak = summoner['hotStreak']
                summoner_obj.flexTT_wins = summoner['wins']
                summoner_obj.flexTT_losses = summoner['losses']
                summoner_obj.flexTT_veteran = summoner['veteran']
                summoner_obj.flexTT_rank = summoner['rank']
                summoner_obj.flexTT_inactive = summoner['inactive']
                summoner_obj.flexTT_freshBlood = summoner['freshBlood']
                summoner_obj.flexTT_leaguePoints = summoner['leaguePoints']

            summoner_obj.save()

        print(Fore.YELLOW + str(count) + Style.RESET_ALL + ' Summoners in ' + tier + ' ' + division + ' ' + queue + ' updated.')

        if count == 205:  # Hit page limit, go to next page.
            page += 1
        elif division == 'IV':  # Last division in tier, end loop.
            continue_next = False
        else:  # Move onto next division.
            if division == 'III':
                division = 'IV'
            if division == 'II':
                division = 'III'
            if division == 'I':
                division = 'II'


def get_all_ranked_summoners(server, queue):
    get_top_ranked(server, queue, 'challenger')
    get_top_ranked(server, queue, 'grandmaster')
    get_top_ranked(server, queue, 'master')
    get_ranked(server, queue, 'DIAMOND')
    get_ranked(server, queue, 'PLATINUM')
    get_ranked(server, queue, 'GOLD')
    get_ranked(server, queue, 'SILVER')
    get_ranked(server, queue, 'BRONZE')
    get_ranked(server, queue, 'IRON')

