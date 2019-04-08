from dashboard.functions.general import *
from dashboard.functions.champions import *
from dashboard.functions.summoners import *
from dashboard.functions.errors import *
from django.conf import settings
from colorama import Fore, Back, Style
import requests, json

def fetchRiotAPI(server, endpoint, version, path, extra='?'):

    if extra != '?':
        extra += '&'

    url = 'https://' + server + '.api.riotgames.com/lol/' + endpoint + '/' + version + '/' + path + extra + 'api_key=' + settings.RIOT_API_KEY
    loadJson = json.loads(json.dumps(requests.get(url).json()))

    print(Fore.MAGENTA + '[RIOT API]: ' + Style.RESET_ALL + url )
    return loadJson

def fetchDDragonAPI(version, type, option1, option2=None, language='en_US',):

    target = ''
    if (option2):
        target += '/' + str(option2)

    url = 'https://ddragon.leagueoflegends.com/cdn/' + version + '/' + type + '/' + language + '/' + option1 + target + '?api_key=' + settings.RIOT_API_KEY
    loadJson = json.loads(json.dumps(requests.get(url).json()))

    print(Fore.MAGENTA + '[RIOT API]: ' + Style.RESET_ALL + url )
    return loadJson

def fetchChatKitAPI(endpoint, value=None):
    instanceId = '5969cdbc-1582-40fa-a851-5aa8bcc6993f'
    url = 'https://us1.pusherplatform.io/services/chatkit_token_provider/chatkit/v3/' + instanceId + '/' + endpoint + '/' + value
    print(Fore.MAGENTA + '[ChatKit API]: ' + Style.RESET_ALL + url )
    return json.loads(json.dumps(requests.get(url).json()))
