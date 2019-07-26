from django.conf import settings
from colorama import Fore, Style
from sentry_sdk import configure_scope
import requests
import json
import time


def fetch_riot_api(server, endpoint, version, path, extra='', session=None):

    # Build the URL that will request the data.
    url = 'https://' + server + '.api.riotgames.com/lol/' + endpoint + '/' + version + '/' + path + extra

    # Print the URL, so it can be easily accessed if necessary.
    # print(Fore.MAGENTA + '[RIOT API]: ' + Style.RESET_ALL + url)

    # Add the Riot API Key to the header of the request for authentication.
    headers = {
        'X-Riot-Token': settings.RIOT_API_KEY,
    }

    # Make the request.
    if session:
        response = session.get(url, headers=headers)

        while response.status_code == 429:
            wait = response.headers['Retry-After']

            print(Fore.YELLOW + '[INFO]: ' + Style.RESET_ALL + 'Rate limit hit. Waiting ' + wait
                  + ' seconds until retrying.')

            time.sleep(int(wait))
            response = session.get(url, headers=headers)

    else:
        response = requests.get(url, headers=headers)

        while response.status_code == 429:
            wait = response.headers['Retry-After']

            print(Fore.YELLOW + '[INFO]: ' + Style.RESET_ALL + 'Rate limit hit. Waiting ' + wait
                  + ' seconds until retrying.')

            time.sleep(int(wait))
            response = requests.get(url, headers=headers)

    if response.status_code != 404:

        # Parse the response so it's usable.
        parsed_response = json.loads(json.dumps(response.json()))

        # Add the JSON to the Sentry reporting scope, will help if an error pops up later.
        with configure_scope() as scope:
            scope.set_extra('JSON', parsed_response)

        if 'status' in parsed_response: # Check if there is an error code of 500, and then try again if so.
            if parsed_response['status']['status_code'] == 500:

                # Make the request.
                response = requests.get(url, headers=headers)

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
    # Depending on the values given, adjust the target variable to accommodate.
    target = ''
    if option2:
        target += '/' + str(option2)

    # Build the URL that will request the data.
    url = 'https://ddragon.leagueoflegends.com/cdn/' + version + '/' + method + '/' + language + '/' \
          + option1 + target

    # Print the URL, so it can be easily accessed if necessary.
    print(Fore.MAGENTA + '[DDRAGON API]: ' + Style.RESET_ALL + url)

    # Add the Riot API Key to the header of the request for authentication.
    headers = {
        'X-Riot-Token': settings.RIOT_API_KEY,
    }

    # Return the response from the API.
    return json.loads(json.dumps(requests.get(url, headers=headers).json()))


def fetch_chatkit_api(endpoint, value=None):
    instance_id = '5969cdbc-1582-40fa-a851-5aa8bcc6993f'
    url = 'https://us1.pusherplatform.io/services/chatkit_token_provider/chatkit/v3/' + instance_id + '/' \
          + endpoint + '/' + value
    print(Fore.MAGENTA + '[ChatKit API]: ' + Style.RESET_ALL + url)
    return json.loads(json.dumps(requests.get(url).json()))
