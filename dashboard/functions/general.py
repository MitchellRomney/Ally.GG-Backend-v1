from colorama import Fore, Style
import requests
import json


def get_latest_version():

    # Fetch list of all versions from the Riot API.
    version_list = json.loads(json.dumps(requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()))

    # Print the request.
    print(Fore.MAGENTA + '[DDRAGON API]: ' + Style.RESET_ALL + 'https://ddragon.leagueoflegends.com/api/versions.json')

    # Return the latest version in the version list.
    return version_list[0]
