from django.conf import settings
from colorama import Fore, Style
from sentry_sdk import configure_scope
import requests
import json
import time


def fetch_riot_api(server, endpoint, version, path, extra='', session=None):
    # Build the URL that will request the data.
    url = 'https://' + server + '.api.riotgames.com/lol/' + endpoint + '/' + version + '/' + path + extra

    # Add the Riot API Key to the header of the request for authentication.
    headers = {
        'X-Riot-Token': settings.RIOT_API_KEY,
    }

    # Make the request.
    if session:
        response = session.get(url, headers=headers)

        attempt = 0

        while response.status_code == 500 or response.status_code == 503 or response.status_code == 429:
            if response.status_code == 429:
                wait = response.headers['Retry-After']
                limit_type = response.headers['X-Rate-Limit-Type']

                if limit_type == 'application':
                    limit_info = 'Limit: ' + response.headers['X-App-Rate-Limit'] \
                                 + '. Count: ' + response.headers['X-App-Rate-Limit-Count']
                else:
                    limit_info = 'Limit: ' + response.headers['X-Method-Rate-Limit'] \
                                 + '. Count: ' + response.headers['X-Method-Rate-Limit-Count']

                print(Fore.YELLOW + '[INFO]: ' + Style.RESET_ALL
                      + limit_type.capitalize() + ' rate limit hit. [' + endpoint + '/' + version + '/' + path + '] '
                      + limit_info
                      + ' | Waiting ' + wait + ' seconds until retrying.')

                time.sleep(int(wait))
                response = session.get(url, headers=headers)

            else:

                attempt += 1

                print(Fore.YELLOW + '[INFO]: ' + Style.RESET_ALL + 'Server Unavailable. Trying again. (Attempt '
                      + str(attempt) + ')')

                time.sleep(1)
                response = session.get(url, headers=headers)

                if response.status_code == 500 or response.status_code == 503 and attempt >= 10:
                    print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + 'Server Unavailable. Max attempt hit, skipping.')
                    return None

    else:
        response = requests.get(url, headers=headers)

        attempt = 0

        while response.status_code == 500 or response.status_code == 503 or response.status_code == 429:
            if response.status_code == 429:
                wait = response.headers['Retry-After']
                limit_type = response.headers['X-Rate-Limit-Type']

                if limit_type == 'application':
                    limit_info = 'Limit: ' + response.headers['X-App-Rate-Limit'] \
                                 + '. Count: ' + response.headers['X-App-Rate-Limit-Count']
                else:
                    limit_info = 'Limit: ' + response.headers['X-Method-Rate-Limit'] \
                                 + '. Count: ' + response.headers['X-Method-Rate-Limit-Count']

                print(Fore.YELLOW + '[INFO]: ' + Style.RESET_ALL
                      + limit_type.capitalize() + ' rate limit hit. [' + endpoint + '/' + version + '/' + path + '] '
                      + limit_info
                      + ' | Waiting ' + wait + ' seconds until retrying.')

                time.sleep(int(wait))
                response = requests.get(url, headers=headers)

            else:

                attempt += 1

                print(Fore.YELLOW + '[INFO]: ' + Style.RESET_ALL + 'Server Unavailable. Trying again. (Attempt '
                      + str(attempt) + ')')

                time.sleep(1)
                response = requests.get(url, headers=headers)

                if response.status_code == 500 or response.status_code == 503 and attempt >= 10:
                    print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + 'Server Unavailable. Max attempt hit, skipping.')
                    return None

    if response.status_code != 404:

        # Parse the response so it's usable.
        parsed_response = json.loads(json.dumps(response.json()))

        if 'status' in parsed_response:  # If the response is STILL an error, report it.
            with configure_scope() as scope:
                scope.set_extra('Error Response', parsed_response)
            print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + parsed_response['status']['message'] + '.')
            return {'isError': True, 'message': parsed_response['status']['message'], 'ignore': False}

        # Return the API response.
        return parsed_response

    else:
        # If Riot API returns 404, return None.
        return None


def fetch_ddragon_api(version, method, option1, option2=None, language='en_US', ):
    target = '/' + str(option2) if option2 else ''

    # Build the URL that will request the data.
    url = 'https://ddragon.leagueoflegends.com/cdn/' + version + '/' + method + '/' + language + '/' \
          + option1 + target

    # Add the Riot API Key to the header of the request for authentication.
    headers = {
        'X-Riot-Token': settings.RIOT_API_KEY,
    }

    # Return the response from the API.
    return json.loads(json.dumps(requests.get(url, headers=headers).json()))
