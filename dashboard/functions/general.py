from colorama import Fore, Style
import requests
import json


def get_latest_version():
    version_list = json.loads(json.dumps(requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()))
    print(Fore.MAGENTA + '[DDRAGON API]: ' + Style.RESET_ALL + 'https://ddragon.leagueoflegends.com/api/versions.json')
    return version_list[0]