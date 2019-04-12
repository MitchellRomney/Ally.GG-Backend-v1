from django.conf import settings
from colorama import Fore, Style
import requests
import json


def fetch_riot_api(server, endpoint, version, path, extra='?'):
    if extra != '?':
        extra += '&'

    url = 'https://' + server + '.api.riotgames.com/lol/' + endpoint + '/' + version + '/' + path + extra \
          + 'api_key=' + settings.RIOT_API_KEY

    print(Fore.MAGENTA + '[RIOT API]: ' + Style.RESET_ALL + url)
    return json.loads(json.dumps(requests.get(url).json()))


def fetch_ddragon_api(version, method, option1, option2=None, language='en_US', ):
    target = ''
    target += '/' + str(option2) if option2 else None

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
