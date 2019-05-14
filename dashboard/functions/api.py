from django.conf import settings
from colorama import Fore, Style
from sentry_sdk import configure_scope
import requests
import json


def fetch_riot_api(server, endpoint, version, path, extra=''):

    # Build the URL that will request the data.
    url = 'https://' + server + '.api.riotgames.com/lol/' + endpoint + '/' + version + '/' + path + extra

    # Print the URL, so it can be easily accessed if necessary.
    # print(Fore.MAGENTA + '[RIOT API]: ' + Style.RESET_ALL + url)

    # Add the Riot API Key to the header of the request for authentication.
    headers = {
        'X-Riot-Token': settings.RIOT_API_KEY,
    }

    # Make the request.
    response = requests.get(url, headers=headers)

    # Print the Rate Limit and App Limit Counts to keep track of limits.
    # if 'X-Method-Rate-Limit-Count' in response.headers:
    #     print(Fore.MAGENTA + 'App Rate Limit Count: '
    #           + Style.RESET_ALL + response.headers['X-App-Rate-Limit-Count']
    #           + Fore.MAGENTA + ' / Method Rate Limit Count: '
    #           + Style.RESET_ALL + response.headers['X-Method-Rate-Limit-Count'])
    # elif 'X-App-Rate-Limit-Count' in response.headers:
    #     print(Fore.MAGENTA + 'App Rate Limit Count: '
    #           + Style.RESET_ALL + response.headers['X-App-Rate-Limit-Count'])

    # Parse the response so it's usable.
    parsed_response = json.loads(json.dumps(response.json()))

    # If status is in the response, that means there is an error. Print and report it.
    if 'status' in parsed_response:
        with configure_scope() as scope:
            scope.set_extra('Error Response', parsed_response)
        print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + parsed_response['status']['message'] + '.')
        return {'isError': True, 'message': parsed_response['status']['message'], 'ignore': False}

    # Add the JSON to the Sentry reporting scope, will help if an error pops up later.
    with configure_scope() as scope:
        scope.set_extra('JSON', parsed_response)

    # Return the API response.
    return parsed_response


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
