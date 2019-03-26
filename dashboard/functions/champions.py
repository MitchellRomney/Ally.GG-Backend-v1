from dashboard.models import *
from dashboard.functions.general import *
from dashboard.functions.summoners import *
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.utils import timezone
from itertools import islice
from datetime import datetime
import requests, json

def updateChampions(version):
    championsInfo = fetchDDragonAPI(version, 'data', 'champion.json')
    for champion, value in championsInfo['data'].items():

        existingChampion = Champion.objects.filter(key=value['key'])

        if existingChampion.count() == 0: # If champion doesn't exist in database.

            newChampion = Champion(
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

            newChampion.save()

            print('New champion added: ' + value['name'])

        else: # If champion DOES exist already, update itself.
            existingChampion = Champion.objects.get(key=value['key'])

            if existingChampion.version != version:

                exsitingChampion.version = value['version']
                exsitingChampion.champId = value['id']
                exsitingChampion.name = value['name']
                exsitingChampion.key = value['key']
                exsitingChampion.title = value['title']
                exsitingChampion.blurb = value['blurb']
                exsitingChampion.info_attack = value['info']['attack']
                exsitingChampion.info_defense = value['info']['defense']
                exsitingChampion.info_magic = value['info']['magic']
                exsitingChampion.info_difficulty = value['info']['difficulty']

                # Images
                exsitingChampion.image_full = value['image']['full']
                exsitingChampion.image_sprite = value['image']['sprite']
                exsitingChampion.image_group = value['image']['group']
                exsitingChampion.image_x = value['image']['x']
                exsitingChampion.image_y = value['image']['y']
                exsitingChampion.image_w = value['image']['w']
                exsitingChampion.image_h = value['image']['h']

                # Stats & Info
                exsitingChampion.tags = value['tags']
                exsitingChampion.partype = value['partype']
                exsitingChampion.stats_hp = value['stats']['hp']
                exsitingChampion.stats_hpperlevel = value['stats']['hpperlevel']
                exsitingChampion.stats_mp = value['stats']['mp']
                exsitingChampion.stats_mpperlevel = value['stats']['mpperlevel']
                exsitingChampion.stats_movespeed = value['stats']['movespeed']
                exsitingChampion.stats_armor = value['stats']['armor']
                exsitingChampion.stats_armorperlevel = value['stats']['armorperlevel']
                exsitingChampion.stats_spellblock = value['stats']['spellblock']
                exsitingChampion.stats_spellblockperlevel = value['stats']['spellblockperlevel']
                exsitingChampion.stats_attackrange = value['stats']['attackrange']
                exsitingChampion.stats_hpregen = value['stats']['hpregen']
                exsitingChampion.stats_hpregenperlevel = value['stats']['hpregenperlevel']
                exsitingChampion.stats_mpregen = value['stats']['mpregen']
                exsitingChampion.stats_mpregenperlevel = value['stats']['mpregenperlevel']
                exsitingChampion.stats_crit = value['stats']['crit']
                exsitingChampion.stats_critperlevel = value['stats']['critperlevel']
                exsitingChampion.stats_attackdamage = value['stats']['attackdamage']
                exsitingChampion.stats_attackdamageperlevel = value['stats']['attackdamageperlevel']
                exsitingChampion.stats_attackspeedperlevel = value['stats']['attackspeedperlevel']
                exsitingChampion.stats_attackspeed = value['stats']['attackspeed']

                print('Champion updated: ' + existingChampion.name)

            else:
                print('Champion already up to date: ' + existingChampion.name)
