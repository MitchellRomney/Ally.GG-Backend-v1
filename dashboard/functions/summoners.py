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
    ranked_info = fetch_riot_api('OC1', 'league', 'v4', 'positions/by-summoner/' + summoner.summonerId)

    # Iterate through the different Ranked Queues.
    for queue in ranked_info:

        # If the Summoner is ranked in SoloQ, update the SoloQ information.
        if queue['queueType'] == 'RANKED_SOLO_5x5':
            summoner.soloQ_leagueId = queue['leagueId']
            summoner.soloQ_leagueName = queue['leagueName']
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
            summoner.flexSR_leagueName = queue['leagueName']
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
            summoner.flexTT_leagueName = queue['leagueName']
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
