from dashboard.functions.summoners import *
from dashboard.models import *
from colorama import Fore, Style


def update_champions(version):
    champions_info = fetch_ddragon_api(version, 'data', 'champion.json')
    for champion, value in champions_info['data'].items():

        existing_champion = Champion.objects.filter(key=value['key'])

        if existing_champion.count() == 0:  # If champion doesn't exist in database.

            new_champion = Champion(
                version=value['version'],
                champId=value['id'],
                name=value['name'],
                key=value['key'],
                title=value['title'],
                blurb=value['blurb'],
                info_attack=value['info']['attack'],
                info_defense=value['info']['defense'],
                info_magic=value['info']['magic'],
                info_difficulty=value['info']['difficulty'],

                # Images
                image_full=value['image']['full'],
                image_sprite=value['image']['sprite'],
                image_group=value['image']['group'],
                image_x=value['image']['x'],
                image_y=value['image']['y'],
                image_w=value['image']['w'],
                image_h=value['image']['h'],

                # Stats & Info
                tags=value['tags'],
                partype=value['partype'],
                stats_hp=value['stats']['hp'],
                stats_hpperlevel=value['stats']['hpperlevel'],
                stats_mp=value['stats']['mp'],
                stats_mpperlevel=value['stats']['mpperlevel'],
                stats_movespeed=value['stats']['movespeed'],
                stats_armor=value['stats']['armor'],
                stats_armorperlevel=value['stats']['armorperlevel'],
                stats_spellblock=value['stats']['spellblock'],
                stats_spellblockperlevel=value['stats']['spellblockperlevel'],
                stats_attackrange=value['stats']['attackrange'],
                stats_hpregen=value['stats']['hpregen'],
                stats_hpregenperlevel=value['stats']['hpregenperlevel'],
                stats_mpregen=value['stats']['mpregen'],
                stats_mpregenperlevel=value['stats']['mpregenperlevel'],
                stats_crit=value['stats']['crit'],
                stats_critperlevel=value['stats']['critperlevel'],
                stats_attackdamage=value['stats']['attackdamage'],
                stats_attackdamageperlevel=value['stats']['attackdamageperlevel'],
                stats_attackspeedperlevel=value['stats']['attackspeedperlevel'],
                stats_attackspeed=value['stats']['attackspeed'],
            )

            new_champion.save()

            print(Fore.GREEN + 'New champion added: ' + Style.RESET_ALL + value['name'])

        else:  # If champion DOES exist already, update itself.
            existing_champion = Champion.objects.get(key=value['key'])

            if existing_champion.version != version:

                existing_champion.version = value['version']
                existing_champion.champId = value['id']
                existing_champion.name = value['name']
                existing_champion.key = value['key']
                existing_champion.title = value['title']
                existing_champion.blurb = value['blurb']
                existing_champion.info_attack = value['info']['attack']
                existing_champion.info_defense = value['info']['defense']
                existing_champion.info_magic = value['info']['magic']
                existing_champion.info_difficulty = value['info']['difficulty']

                # Images
                existing_champion.image_full = value['image']['full']
                existing_champion.image_sprite = value['image']['sprite']
                existing_champion.image_group = value['image']['group']
                existing_champion.image_x = value['image']['x']
                existing_champion.image_y = value['image']['y']
                existing_champion.image_w = value['image']['w']
                existing_champion.image_h = value['image']['h']

                # Stats & Info
                existing_champion.tags = value['tags']
                existing_champion.partype = value['partype']
                existing_champion.stats_hp = value['stats']['hp']
                existing_champion.stats_hpperlevel = value['stats']['hpperlevel']
                existing_champion.stats_mp = value['stats']['mp']
                existing_champion.stats_mpperlevel = value['stats']['mpperlevel']
                existing_champion.stats_movespeed = value['stats']['movespeed']
                existing_champion.stats_armor = value['stats']['armor']
                existing_champion.stats_armorperlevel = value['stats']['armorperlevel']
                existing_champion.stats_spellblock = value['stats']['spellblock']
                existing_champion.stats_spellblockperlevel = value['stats']['spellblockperlevel']
                existing_champion.stats_attackrange = value['stats']['attackrange']
                existing_champion.stats_hpregen = value['stats']['hpregen']
                existing_champion.stats_hpregenperlevel = value['stats']['hpregenperlevel']
                existing_champion.stats_mpregen = value['stats']['mpregen']
                existing_champion.stats_mpregenperlevel = value['stats']['mpregenperlevel']
                existing_champion.stats_crit = value['stats']['crit']
                existing_champion.stats_critperlevel = value['stats']['critperlevel']
                existing_champion.stats_attackdamage = value['stats']['attackdamage']
                existing_champion.stats_attackdamageperlevel = value['stats']['attackdamageperlevel']
                existing_champion.stats_attackspeedperlevel = value['stats']['attackspeedperlevel']
                existing_champion.stats_attackspeed = value['stats']['attackspeed']

                print(Fore.YELLOW + 'Champion updated: ' + Style.RESET_ALL + existing_champion.name)

            else:
                print(Fore.CYAN + 'Champion already up to date: ' + Style.RESET_ALL + existing_champion.name)
