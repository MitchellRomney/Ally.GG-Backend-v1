from dashboard.functions.api import *
from dashboard.models import *
from django.utils import timezone
from django.db import IntegrityError
from colorama import Fore, Style


def add_summoner(method, value):
    # TODO: If Summoner is being added from a ranked game, do ranked pull. Otherwise do normal pull.
    if method == 'SummonerId':
        existing_summoner = Summoner.objects.filter(summonerId=value)
        if existing_summoner.count() == 0:
            summoner_info = fetch_riot_api('OC1', 'league', 'v4', 'positions/by-summoner/' + value)
            if summoner_info:  # Will be empty if user has never played ranked.
                try:
                    summoner = Summoner.objects.create(
                        # General
                        summonerName=summoner_info[0]['summonerName'],
                        summonerId=summoner_info[0]['summonerId'],
                        server='OC1',  # TODO: Need to pass through server and set this dynamically.

                        # System
                        date_created=timezone.now(),
                    )

                except IntegrityError:
                    existing_summoner = Summoner.objects.get(summonerId=summoner_info['id'])
                    return {
                        'isError': True,
                        'errorMessage': 'Summoner already exists.',
                        'summonerId': existing_summoner.summonerId
                    }

                for queue in summoner_info:
                    if queue['queueType'] == 'RANKED_SOLO_5x5':
                        summoner.soloQ_leagueId = queue['leagueId'] \
                            if summoner.soloQ_leagueId != queue['leagueId'] else summoner.soloQ_leagueId
                        summoner.soloQ_leagueName = queue['leagueName'] \
                            if summoner.soloQ_leagueName != queue['leagueName'] else summoner.soloQ_leagueName
                        summoner.soloQ_tier = RankedTier.objects.get(key=queue['tier']) \
                            if summoner.soloQ_tier != queue['tier'] else summoner.soloQ_tier
                        summoner.soloQ_hotStreak = queue['hotStreak'] \
                            if summoner.soloQ_hotStreak != queue['hotStreak'] else summoner.soloQ_hotStreak
                        summoner.soloQ_wins = queue['wins'] \
                            if summoner.soloQ_wins != queue['wins'] else summoner.soloQ_wins
                        summoner.soloQ_losses = queue['losses'] \
                            if summoner.soloQ_losses != queue['losses'] else summoner.soloQ_losses
                        summoner.soloQ_veteran = queue['veteran'] \
                            if summoner.soloQ_veteran != queue['veteran'] else summoner.soloQ_veteran
                        summoner.soloQ_rank = queue['rank'] \
                            if summoner.soloQ_rank != queue['rank'] else summoner.soloQ_rank
                        summoner.soloQ_inactive = queue['inactive'] \
                            if summoner.soloQ_inactive != queue['inactive'] else summoner.soloQ_inactive
                        summoner.soloQ_freshBlood = queue['freshBlood'] \
                            if summoner.soloQ_freshBlood != queue['freshBlood'] else summoner.soloQ_freshBlood
                        summoner.soloQ_leaguePoints = queue['leaguePoints'] \
                            if summoner.soloQ_leaguePoints != queue['leaguePoints'] else summoner.soloQ_leaguePoints
                    if queue['queueType'] == 'RANKED_FLEX_SR':
                        summoner.flexSR_leagueId = queue['leagueId'] \
                            if summoner.flexSR_leagueId != queue['leagueId'] else summoner.flexSR_leagueId
                        summoner.flexSR_leagueName = queue['leagueName'] \
                            if summoner.flexSR_leagueName != queue['leagueName'] else summoner.flexSR_leagueName
                        summoner.flexSR_tier = RankedTier.objects.get(key=queue['tier']) \
                            if summoner.flexSR_tier != queue['tier'] else summoner.flexSR_tier
                        summoner.flexSR_hotStreak = queue['hotStreak'] \
                            if summoner.flexSR_hotStreak != queue['hotStreak'] else summoner.flexSR_hotStreak
                        summoner.flexSR_wins = queue['wins'] \
                            if summoner.flexSR_wins != queue['wins'] else summoner.flexSR_wins
                        summoner.flexSR_losses = queue['losses'] \
                            if summoner.flexSR_losses != queue['losses'] else summoner.flexSR_losses
                        summoner.flexSR_veteran = queue['veteran'] \
                            if summoner.flexSR_veteran != queue['veteran'] else summoner.flexSR_veteran
                        summoner.flexSR_rank = queue['rank'] \
                            if summoner.flexSR_rank != queue['rank'] else summoner.flexSR_rank
                        summoner.flexSR_inactive = queue['inactive'] \
                            if summoner.flexSR_inactive != queue['inactive'] else summoner.flexSR_inactive
                        summoner.flexSR_freshBlood = queue['freshBlood'] \
                            if summoner.flexSR_freshBlood != queue['freshBlood'] else summoner.flexSR_freshBlood
                        summoner.flexSR_leaguePoints = queue['leaguePoints'] \
                            if summoner.flexSR_leaguePoints != queue['leaguePoints'] else summoner.flexSR_leaguePoints
                    if queue['queueType'] == 'RANKED_FLEX_TT':
                        summoner.flexTT_leagueId = queue['leagueId'] \
                            if summoner.flexTT_leagueId != queue['leagueId'] else summoner.flexTT_leagueId
                        summoner.flexTT_leagueName = queue['leagueName'] \
                            if summoner.flexTT_leagueName != queue['leagueName'] else summoner.flexTT_leagueName
                        summoner.flexTT_tier = RankedTier.objects.get(key=queue['tier']) \
                            if summoner.flexTT_tier != queue['tier'] else summoner.flexTT_tier
                        summoner.flexTT_hotStreak = queue['hotStreak'] \
                            if summoner.flexTT_hotStreak != queue['hotStreak'] else summoner.flexTT_hotStreak
                        summoner.flexTT_wins = queue['wins'] \
                            if summoner.flexTT_wins != queue['wins'] else summoner.flexTT_wins
                        summoner.flexTT_losses = queue['losses'] \
                            if summoner.flexTT_losses != queue['losses'] else summoner.flexTT_losses
                        summoner.flexTT_veteran = queue['veteran'] \
                            if summoner.flexTT_veteran != queue['veteran'] else summoner.flexTT_veteran
                        summoner.flexTT_rank = queue['rank'] \
                            if summoner.flexTT_rank != queue['rank'] else summoner.flexTT_rank
                        summoner.flexTT_inactive = queue['inactive'] \
                            if summoner.flexTT_inactive != queue['inactive'] else summoner.flexTT_inactive
                        summoner.flexTT_freshBlood = queue['freshBlood'] \
                            if summoner.flexTT_freshBlood != queue['freshBlood'] else summoner.flexTT_freshBlood
                        summoner.flexTT_leaguePoints = queue['leaguePoints'] \
                            if summoner.flexTT_leaguePoints != queue['leaguePoints'] else summoner.flexTT_leaguePoints

            else:  # User has never played ranked, need to get info directly.
                summoner_info = fetch_riot_api('OC1', 'summoner', 'v4', 'summoners/' + value)
                existing_summoner = Summoner.objects.filter(summonerId=summoner_info['id'])

                if existing_summoner.count() != 0:
                    return {
                        'isError': True,
                        'errorMessage': 'Summoner already exists.',
                        'summonerId': existing_summoner.summonerId
                    }

                if 'status' in summoner_info:
                    print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + summoner_info['status']['message'] + '.')
                    return {
                        'isError': True,
                        'errorMessage': summoner_info['status']['message'],
                        'summonerId': None
                    }

                try:
                    summoner = Summoner.objects.create(
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
                except IntegrityError:
                    existing_summoner = Summoner.objects.get(summonerId=summoner_info['id'])
                    return {
                        'isError': True,
                        'errorMessage': 'Summoner already exists.',
                        'summonerId': existing_summoner.summonerId
                    }

            print(Fore.GREEN + 'New Summoner Created: ' + Style.RESET_ALL + summoner.summonerName)
            return {
                'isError': False,
                'errorMessage': '',
                'summonerId': summoner.summonerId
            }

        else:
            return {
                'isError': True,
                'errorMessage': 'Summoner already exists.',
                'summonerId': existing_summoner.summonerId
            }
    else:
        summoner_info = fetch_riot_api('OC1', 'summoner', 'v4', 'summoners/by-name/' + value)
        existing_summoner = Summoner.objects.filter(summonerId=summoner_info['id'])

        if existing_summoner.count() != 0:
            return {
                'isError': True,
                'errorMessage': 'Summoner already exists.',
                'summonerId': existing_summoner.summonerId
            }

        if 'status' in summoner_info:
            print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + summoner_info['status']['message'] + '.')
            return {
                'isError': True,
                'errorMessage': summoner_info['status']['message'],
                'summonerId': None
            }

        try:
            summoner = Summoner.objects.create(
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
        except IntegrityError:
            existing_summoner = Summoner.objects.get(summonerId=summoner_info['id'])
            return {
                'isError': True,
                'errorMessage': 'Summoner already exists.',
                'summonerId': existing_summoner.summonerId
            }

        print(Fore.GREEN + 'New Summoner Created: ' + Style.RESET_ALL + summoner.summonerName)
        return {
            'isError': False,
            'errorMessage': '',
            'summonerId': summoner.summonerId
        }


def update_summoner(summonerId):
    print(summonerId)
    summoner = Summoner.objects.get(summonerId=summonerId)
    print(Fore.YELLOW + 'Updating Summoner: ' + Style.RESET_ALL + summoner.summonerName)

    summoner_info = fetch_riot_api('OC1', 'summoner', 'v4', 'summoners/' + summonerId)
    if 'status' in summoner_info:
        print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + summoner_info['status']['message'] + '.')
        return {'isError': True, 'errorMessage': summoner_info['status']['message']}

    summoner.summonerName = summoner_info['name'] \
        if summoner.summonerName != summoner_info['name'] else summoner.summonerName
    summoner.profileIconId = summoner_info['profileIconId'] \
        if summoner.profileIconId != summoner_info['profileIconId'] else summoner.profileIconId
    summoner.summonerLevel = summoner_info['summonerLevel'] \
        if summoner.summonerName != summoner_info['summonerLevel'] else summoner.summonerName

    summoner.puuid = summoner_info['puuid'] \
        if summoner.puuid is None else summoner.puuid
    summoner.accountId = summoner_info['accountId'] \
        if summoner.accountId is None else summoner.accountId

    update_summoner_ranked(summoner)

    return {
        'message': 'Summoner Updated!',
        'summonerId': summoner.summonerId,
        'isError': False
    }


def update_summoner_ranked(summoner):
    print(Fore.YELLOW + 'Updating Summoner Ranked Information: ' + Style.RESET_ALL + summoner.summonerName)
    ranked_info = fetch_riot_api('OC1', 'league', 'v4', 'positions/by-summoner/' + summoner.summonerId)
    if 'status' in ranked_info:
        print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + ranked_info['status']['message'] + '.')
        return {'isError': True, 'errorMessage': ranked_info['status']['message']}

    for queue in ranked_info:
        if queue['queueType'] == 'RANKED_SOLO_5x5':
            summoner.soloQ_leagueId = queue['leagueId'] \
                if summoner.soloQ_leagueId != queue['leagueId'] else summoner.soloQ_leagueId
            summoner.soloQ_leagueName = queue['leagueName'] \
                if summoner.soloQ_leagueName != queue['leagueName'] else summoner.soloQ_leagueName
            summoner.soloQ_tier = RankedTier.objects.get(key=queue['tier']) \
                if summoner.soloQ_tier != queue['tier'] else summoner.soloQ_tier
            summoner.soloQ_hotStreak = queue['hotStreak'] \
                if summoner.soloQ_hotStreak != queue['hotStreak'] else summoner.soloQ_hotStreak
            summoner.soloQ_wins = queue['wins'] \
                if summoner.soloQ_wins != queue['wins'] else summoner.soloQ_wins
            summoner.soloQ_losses = queue['losses'] \
                if summoner.soloQ_losses != queue['losses'] else summoner.soloQ_losses
            summoner.soloQ_veteran = queue['veteran'] \
                if summoner.soloQ_veteran != queue['veteran'] else summoner.soloQ_veteran
            summoner.soloQ_rank = queue['rank'] \
                if summoner.soloQ_rank != queue['rank'] else summoner.soloQ_rank
            summoner.soloQ_inactive = queue['inactive'] \
                if summoner.soloQ_inactive != queue['inactive'] else summoner.soloQ_inactive
            summoner.soloQ_freshBlood = queue['freshBlood'] \
                if summoner.soloQ_freshBlood != queue['freshBlood'] else summoner.soloQ_freshBlood
            summoner.soloQ_leaguePoints = queue['leaguePoints'] \
                if summoner.soloQ_leaguePoints != queue['leaguePoints'] else summoner.soloQ_leaguePoints
        if queue['queueType'] == 'RANKED_FLEX_SR':
            summoner.flexSR_leagueId = queue['leagueId'] \
                if summoner.flexSR_leagueId != queue['leagueId'] else summoner.flexSR_leagueId
            summoner.flexSR_leagueName = queue['leagueName'] \
                if summoner.flexSR_leagueName != queue['leagueName'] else summoner.flexSR_leagueName
            summoner.flexSR_tier = RankedTier.objects.get(key=queue['tier']) \
                if summoner.flexSR_tier != queue['tier'] else summoner.flexSR_tier
            summoner.flexSR_hotStreak = queue['hotStreak'] \
                if summoner.flexSR_hotStreak != queue['hotStreak'] else summoner.flexSR_hotStreak
            summoner.flexSR_wins = queue['wins'] \
                if summoner.flexSR_wins != queue['wins'] else summoner.flexSR_wins
            summoner.flexSR_losses = queue['losses'] \
                if summoner.flexSR_losses != queue['losses'] else summoner.flexSR_losses
            summoner.flexSR_veteran = queue['veteran'] \
                if summoner.flexSR_veteran != queue['veteran'] else summoner.flexSR_veteran
            summoner.flexSR_rank = queue['rank'] \
                if summoner.flexSR_rank != queue['rank'] else summoner.flexSR_rank
            summoner.flexSR_inactive = queue['inactive'] \
                if summoner.flexSR_inactive != queue['inactive'] else summoner.flexSR_inactive
            summoner.flexSR_freshBlood = queue['freshBlood'] \
                if summoner.flexSR_freshBlood != queue['freshBlood'] else summoner.flexSR_freshBlood
            summoner.flexSR_leaguePoints = queue['leaguePoints'] \
                if summoner.flexSR_leaguePoints != queue['leaguePoints'] else summoner.flexSR_leaguePoints
        if queue['queueType'] == 'RANKED_FLEX_TT':
            summoner.flexTT_leagueId = queue['leagueId'] \
                if summoner.flexTT_leagueId != queue['leagueId'] else summoner.flexTT_leagueId
            summoner.flexTT_leagueName = queue['leagueName'] \
                if summoner.flexTT_leagueName != queue['leagueName'] else summoner.flexTT_leagueName
            summoner.flexTT_tier = RankedTier.objects.get(key=queue['tier']) \
                if summoner.flexTT_tier != queue['tier'] else summoner.flexTT_tier
            summoner.flexTT_hotStreak = queue['hotStreak'] \
                if summoner.flexTT_hotStreak != queue['hotStreak'] else summoner.flexTT_hotStreak
            summoner.flexTT_wins = queue['wins'] \
                if summoner.flexTT_wins != queue['wins'] else summoner.flexTT_wins
            summoner.flexTT_losses = queue['losses'] \
                if summoner.flexTT_losses != queue['losses'] else summoner.flexTT_losses
            summoner.flexTT_veteran = queue['veteran'] \
                if summoner.flexTT_veteran != queue['veteran'] else summoner.flexTT_veteran
            summoner.flexTT_rank = queue['rank'] \
                if summoner.flexTT_rank != queue['rank'] else summoner.flexTT_rank
            summoner.flexTT_inactive = queue['inactive'] \
                if summoner.flexTT_inactive != queue['inactive'] else summoner.flexTT_inactive
            summoner.flexTT_freshBlood = queue['freshBlood'] \
                if summoner.flexTT_freshBlood != queue['freshBlood'] else summoner.flexTT_freshBlood
            summoner.flexTT_leaguePoints = queue['leaguePoints'] \
                if summoner.flexTT_leaguePoints != queue['leaguePoints'] else summoner.flexTT_leaguePoints

    summoner.date_updated = timezone.now()

    summoner.save()
