from django.conf import settings
from colorama import Fore, Style
from sentry_sdk import configure_scope
import requests
import json


def fetch_riot_api(server, endpoint, version, path, extra='?'):
    if extra != '?':
        extra += '&'

    url = 'https://' + server + '.api.riotgames.com/lol/' + endpoint + '/' + version + '/' + path + extra \
          + 'api_key=' + settings.RIOT_API_KEY

    print(Fore.MAGENTA + '[RIOT API]: '
          + Style.RESET_ALL + url)

    response = requests.get(url)

    if 'X-Method-Rate-Limit-Count' in response.headers:
        print(Fore.MAGENTA + 'App Rate Limit Count: '
              + Style.RESET_ALL + response.headers['X-App-Rate-Limit-Count']
              + Fore.MAGENTA + ' / Method Rate Limit Count: '
              + Style.RESET_ALL + response.headers['X-Method-Rate-Limit-Count'])
    elif 'X-App-Rate-Limit-Count' in response.headers:
        print(Fore.MAGENTA + 'App Rate Limit Count: '
              + Style.RESET_ALL + response.headers['X-App-Rate-Limit-Count'])

    parsed_response = json.loads(json.dumps(response.json()))

    if 'status' in parsed_response:
        with configure_scope() as scope:
            scope.set_extra('Error Response', parsed_response)
        print(Fore.RED + '[ERROR]: ' + Style.RESET_ALL + parsed_response['status']['message'] + '.')
        return {'isError': True, 'errorMessage': parsed_response['status']['message'], 'ignore': False}

    with configure_scope() as scope:
        scope.set_extra('JSON', parsed_response)

    return parsed_response


def fetch_ddragon_api(version, method, option1, option2=None, language='en_US', ):
    target = ''
    if option2:
        target += '/' + str(option2)

    url = 'https://ddragon.leagueoflegends.com/cdn/' + version + '/' + method + '/' + language + '/' \
          + option1 + target + '?api_key=' + settings.RIOT_API_KEY

    print(Fore.MAGENTA + '[DDRAGON API]: ' + Style.RESET_ALL + url)
    return json.loads(json.dumps(requests.get(url).json()))


def fetch_chatkit_api(endpoint, value=None):
    instance_id = '5969cdbc-1582-40fa-a851-5aa8bcc6993f'
    url = 'https://us1.pusherplatform.io/services/chatkit_token_provider/chatkit/v3/' + instance_id + '/' \
          + endpoint + '/' + value
    print(Fore.MAGENTA + '[ChatKit API]: ' + Style.RESET_ALL + url)
    return json.loads(json.dumps(requests.get(url).json()))
