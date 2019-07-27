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


def is_new_version(current, new):

    current_list = current.split('.')
    new_list = new.split('.')

    if int(new_list[0]) > int(current_list[0]):
        return True
    elif int(new_list[0]) == int(current_list[0]):
        if int(new_list[1]) > int(current_list[1]):
            return True
        elif int(new_list[1]) == int(current_list[1]):
            if int(new_list[2]) > int(current_list[2]):
                return True

    return False
