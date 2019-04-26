from dashboard.functions.summoners import *
from dashboard.models import *
from colorama import Fore, Style


def update_game_data(version):
    check_champions(version)
    check_runes(version)
    check_items(version)
    check_summoner_spells(version)
    check_ranked_tiers()


def check_champions(version):  # Create/Update all champions.
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

                existing_champion.save()

                print(Fore.YELLOW + 'Champion updated: ' + Style.RESET_ALL + existing_champion.name)

            else:
                print(Fore.CYAN + 'Champion already up to date: ' + Style.RESET_ALL + existing_champion.name)


def check_runes(version):  # Create/Update all runes.

    if Rune.objects.filter(runeId=0).count() == 0:
        Rune.objects.create(runeId=0, name="No Rune")

    runes_info = fetch_ddragon_api(version, 'data', 'runesReforged.json')
    for tree in runes_info:
        for slot in tree['slots']:
            for rune in slot['runes']:
                existing_rune = Rune.objects.filter(runeId=rune['id'])

                if existing_rune.count() == 0:  # If rune doesn't exist in database.

                    new_rune = Rune(
                        version=version,
                        runeId=rune['id'],
                        key=rune['key'],
                        icon=rune['icon'],
                        name=rune['name'],
                        shortDesc=rune['shortDesc'],
                        longDesc=rune['longDesc'],
                    )

                    new_rune.save()

                    print(Fore.GREEN + 'New rune added: ' + Style.RESET_ALL + rune['name'])

                else:  # If champion DOES exist already, update itself.
                    existing_rune = Rune.objects.get(runeId=rune['id'])

                    if existing_rune.version != version:
                        existing_rune.runeId = rune['id']
                        existing_rune.key = rune['key']
                        existing_rune.icon = rune['icon']
                        existing_rune.name = rune['name']
                        existing_rune.shortDesc = rune['shortDesc']
                        existing_rune.longDesc = rune['longDesc']

                        existing_rune.save()

                        print(Fore.YELLOW + 'Rune updated: ' + Style.RESET_ALL + existing_rune.name)

                    else:
                        print(Fore.CYAN + 'Rune already up to date: ' + Style.RESET_ALL + existing_rune.name)


def check_items(version):  # Create/Update all items.

    if Item.objects.filter(itemId=0).count() == 0:
        Item.objects.create(itemId=0,name="No Item")

    item_info = fetch_ddragon_api(version, 'data', 'item.json')
    for item, value in item_info['data'].items():
        existing_item = Item.objects.filter(itemId=item)
        if existing_item.count() == 0:
            Item.objects.create(
                itemId=item,
            )
            print(Fore.GREEN + 'New item added: ' + Style.RESET_ALL + value['name'])

        existing_item = Item.objects.get(itemId=item)

        if existing_item.version < version:
            existing_item.version = version
            existing_item.itemId = item
            existing_item.name = value['name']
            existing_item.description = value['description']
            existing_item.colloq = value['colloq']
            existing_item.plaintext = value['plaintext']
            existing_item.consumed = value['consumed'] if 'consumed' in item else False
            existing_item.stacks = value['stacks'] if 'stacks' in item else 0
            existing_item.depth = value['depth'] if 'depth' in item else 0
            existing_item.consumeOnFull = value['consumeOnFull'] if 'consumeOnFull' in item else False
            existing_item.specialRecipe = value['specialRecipe'] if 'specialRecipe' in item else 0
            existing_item.inStore = value['inStore'] if 'inStore' in item else True
            existing_item.hideFromAll = value['hideFromAll'] if 'hideFromAll' in item else False
            existing_item.requiredChampion = value['requiredChampion'] if 'requiredChampion' in item else False
            existing_item.requiredAlly = value['requiredAlly'] if 'requiredAlly' in item else False

            existing_item.image_full = value['image']['full']
            existing_item.image_sprite = value['image']['sprite']
            existing_item.image_group = value['image']['group']
            existing_item.image_x = value['image']['x']
            existing_item.image_y = value['image']['y']
            existing_item.image_w = value['image']['w']
            existing_item.image_h = value['image']['h']

            existing_item.gold_base = value['gold']['base']
            existing_item.gold_purchasable = value['gold']['purchasable']
            existing_item.gold_total = value['gold']['total']
            existing_item.gold_sell = value['gold']['sell']

            existing_item.tags = value['tags'] if 'tags' in value else False

            if 'maps' in value:
                existing_item.maps_1 = value['maps']['1'] if '1' in value['maps'] else False
                existing_item.maps_8 = value['maps']['8'] if '8' in value['maps'] else False
                existing_item.maps_10 = value['maps']['10'] if '10' in value['maps'] else False
                existing_item.maps_11 = value['maps']['11'] if '11' in value['maps'] else False
                existing_item.maps_12 = value['maps']['12'] if '12' in value['maps'] else False

            existing_item.FlatHPPoolMod = value['stats']['FlatHPPoolMod'] if 'FlatHPPoolMod' in value['stats'] else 0
            existing_item.rFlatHPModPerLevel = value['stats']['rFlatHPModPerLevel'] if 'rFlatHPModPerLevel' in value['stats'] else 0
            existing_item.FlatMPPoolMod = value['stats']['FlatMPPoolMod'] if 'FlatMPPoolMod' in value['stats'] else 0
            existing_item.rFlatMPModPerLevel = value['stats'][''] if 'rFlatMPModPerLevel' in value['stats'] else 0
            existing_item.PercentHPPoolMod = value['stats']['PercentHPPoolMod'] if 'PercentHPPoolMod' in value['stats'] else 0
            existing_item.PercentMPPoolMod = value['stats']['PercentMPPoolMod'] if 'PercentMPPoolMod' in value['stats'] else 0
            existing_item.FlatHPRegenMod = value['stats']['FlatHPRegenMod'] if 'FlatHPRegenMod' in value['stats'] else 0
            existing_item.rFlatHPRegenModPerLevel = value['stats']['rFlatHPRegenModPerLevel'] if 'rFlatHPRegenModPerLevel' in value['stats'] else 0
            existing_item.PercentHPRegenMod = value['stats']['PercentHPRegenMod'] if 'PercentHPRegenMod' in value['stats'] else 0
            existing_item.FlatMPRegenMod = value['stats']['FlatMPRegenMod'] if 'FlatMPRegenMod' in value['stats'] else 0
            existing_item.rFlatMPRegenModPerLevel = value['stats']['rFlatMPRegenModPerLevel'] if 'rFlatMPRegenModPerLevel' in value['stats'] else 0
            existing_item.PercentMPRegenMod = value['stats']['PercentMPRegenMod'] if 'PercentMPRegenMod' in value['stats'] else 0
            existing_item.FlatArmorMod = value['stats']['FlatArmorMod'] if 'FlatArmorMod' in value['stats'] else 0
            existing_item.rFlatArmorModPerLevel = value['stats']['rFlatArmorModPerLevel'] if 'rFlatArmorModPerLevel' in value['stats'] else 0
            existing_item.PercentArmorMod = value['stats']['PercentArmorMod'] if 'PercentArmorMod' in value['stats'] else 0
            existing_item.rFlatArmorPenetrationMod = value['stats']['rFlatArmorPenetrationMod'] if 'rFlatArmorPenetrationMod' in value['stats'] else 0
            existing_item.rFlatArmorPenetrationModPerLevel = value['stats']['rFlatArmorPenetrationModPerLevel'] if 'rFlatArmorPenetrationModPerLevel' in value['stats'] else 0
            existing_item.rPercentArmorPenetrationMod = value['stats']['rPercentArmorPenetrationMod'] if 'rPercentArmorPenetrationMod' in value['stats'] else 0
            existing_item.rPercentArmorPenetrationModPerLevel = value['stats']['rPercentArmorPenetrationModPerLevel'] if 'rPercentArmorPenetrationModPerLevel' in value['stats'] else 0
            existing_item.FlatPhysicalDamageMod = value['stats']['FlatPhysicalDamageMod'] if 'FlatPhysicalDamageMod' in value['stats'] else 0
            existing_item.rFlatPhysicalDamageModPerLevel = value['stats']['rFlatPhysicalDamageModPerLevel'] if 'rFlatPhysicalDamageModPerLevel' in value['stats'] else 0
            existing_item.PercentPhysicalDamageMod = value['stats']['PercentPhysicalDamageMod'] if 'PercentPhysicalDamageMod' in value['stats'] else 0
            existing_item.FlatMagicDamageMod = value['stats']['FlatMagicDamageMod'] if 'FlatMagicDamageMod' in value['stats'] else 0
            existing_item.rFlatMagicDamageModPerLevel = value['stats']['rFlatMagicDamageModPerLevel'] if 'rFlatMagicDamageModPerLevel' in value['stats'] else 0
            existing_item.PercentMagicDamageMod = value['stats']['PercentMagicDamageMod'] if 'PercentMagicDamageMod' in value['stats'] else 0
            existing_item.FlatMovementSpeedMod = value['stats']['FlatMovementSpeedMod'] if 'FlatMovementSpeedMod' in value['stats'] else 0
            existing_item.rFlatMovementSpeedModPerLevel = value['stats']['rFlatMovementSpeedModPerLevel'] if 'rFlatMovementSpeedModPerLevel' in value['stats'] else 0
            existing_item.PercentMovementSpeedMod = value['stats']['PercentMovementSpeedMod'] if 'PercentMovementSpeedMod' in value['stats'] else 0
            existing_item.rPercentMovementSpeedModPerLevel = value['stats']['rPercentMovementSpeedModPerLevel'] if 'rPercentMovementSpeedModPerLevel' in value['stats'] else 0
            existing_item.FlatAttackSpeedMod = value['stats']['FlatAttackSpeedMod'] if 'FlatAttackSpeedMod' in value['stats'] else 0
            existing_item.PercentAttackSpeedMod = value['stats']['PercentAttackSpeedMod'] if 'PercentAttackSpeedMod' in value['stats'] else 0
            existing_item.rPercentAttackSpeedModPerLevel = value['stats']['rPercentAttackSpeedModPerLevel'] if 'rPercentAttackSpeedModPerLevel' in value['stats'] else 0
            existing_item.rFlatDodgeMod = value['stats']['rFlatDodgeMod'] if 'rFlatDodgeMod' in value['stats'] else 0
            existing_item.rFlatDodgeModPerLevel = value['stats']['rFlatDodgeModPerLevel'] if 'rFlatDodgeModPerLevel' in value['stats'] else 0
            existing_item.PercentDodgeMod = value['stats']['PercentDodgeMod'] if 'PercentDodgeMod' in value['stats'] else 0
            existing_item.FlatCritChanceMod = value['stats']['FlatCritChanceMod'] if 'FlatCritChanceMod' in value['stats'] else 0
            existing_item.rFlatCritChanceModPerLevel = value['stats']['rFlatCritChanceModPerLevel'] if 'rFlatCritChanceModPerLevel' in value['stats'] else 0
            existing_item.PercentCritChanceMod = value['stats']['PercentCritChanceMod'] if 'PercentCritChanceMod' in value['stats'] else 0
            existing_item.FlatCritDamageMod = value['stats']['FlatCritDamageMod'] if 'FlatCritDamageMod' in value['stats'] else 0
            existing_item.rFlatCritDamageModPerLevel = value['stats']['rFlatCritDamageModPerLevel'] if 'rFlatCritDamageModPerLevel' in value['stats'] else 0
            existing_item.PercentCritDamageMod = value['stats']['PercentCritDamageMod'] if 'PercentCritDamageMod' in value['stats'] else 0
            existing_item.FlatBlockMod = value['stats']['FlatBlockMod'] if 'FlatBlockMod' in value['stats'] else 0
            existing_item.PercentBlockMod = value['stats']['PercentBlockMod'] if 'PercentBlockMod' in value['stats'] else 0
            existing_item.FlatSpellBlockMod = value['stats']['FlatSpellBlockMod'] if 'FlatSpellBlockMod' in value['stats'] else 0
            existing_item.rFlatSpellBlockModPerLevel = value['stats']['rFlatSpellBlockModPerLevel'] if 'rFlatSpellBlockModPerLevel' in value['stats'] else 0
            existing_item.PercentSpellBlockMod = value['stats']['PercentSpellBlockMod'] if 'PercentSpellBlockMod' in value['stats'] else 0
            existing_item.FlatEXPBonus = value['stats']['FlatEXPBonus'] if 'FlatEXPBonus' in value['stats'] else 0
            existing_item.PercentEXPBonus = value['stats']['PercentEXPBonus'] if 'PercentEXPBonus' in value['stats'] else 0
            existing_item.rPercentCooldownMod = value['stats']['rPercentCooldownMod'] if 'rPercentCooldownMod' in value['stats'] else 0
            existing_item.rPercentCooldownModPerLevel = value['stats']['rPercentCooldownModPerLevel'] if 'rPercentCooldownModPerLevel' in value['stats'] else 0
            existing_item.rFlatTimeDeadMod = value['stats']['rFlatTimeDeadMod'] if 'rFlatTimeDeadMod' in value['stats'] else 0
            existing_item.rFlatTimeDeadModPerLevel = value['stats']['rFlatTimeDeadModPerLevel'] if 'rFlatTimeDeadModPerLevel' in value['stats'] else 0
            existing_item.rPercentTimeDeadMod = value['stats']['rPercentTimeDeadMod'] if 'rPercentTimeDeadMod' in value['stats'] else 0
            existing_item.rPercentTimeDeadModPerLevel = value['stats']['rPercentTimeDeadModPerLevel'] if 'rPercentTimeDeadModPerLevel' in value['stats'] else 0
            existing_item.rFlatGoldPer10Mod = value['stats']['rFlatGoldPer10Mod'] if 'rFlatGoldPer10Mod' in value['stats'] else 0
            existing_item.rFlatMagicPenetrationMod = value['stats']['rFlatMagicPenetrationMod'] if 'rFlatMagicPenetrationMod' in value['stats'] else 0
            existing_item.rFlatMagicPenetrationModPerLevel = value['stats']['rFlatMagicPenetrationModPerLevel'] if 'rFlatMagicPenetrationModPerLevel' in value['stats'] else 0
            existing_item.rPercentMagicPenetrationMod = value['stats']['rPercentMagicPenetrationMod'] if 'rPercentMagicPenetrationMod' in value['stats'] else 0
            existing_item.rPercentMagicPenetrationModPerLevel = value['stats']['rPercentMagicPenetrationModPerLevel'] if 'rPercentMagicPenetrationModPerLevel' in value['stats'] else 0
            existing_item.FlatEnergyRegenMod = value['stats']['FlatEnergyRegenMod'] if 'FlatEnergyRegenMod' in value['stats'] else 0
            existing_item.rFlatEnergyRegenModPerLevel = value['stats']['rFlatEnergyRegenModPerLevel'] if 'rFlatEnergyRegenModPerLevel' in value['stats'] else 0
            existing_item.FlatEnergyPoolMod = value['stats']['FlatEnergyPoolMod'] if 'FlatEnergyPoolMod' in value['stats'] else 0
            existing_item.rFlatEnergyModPerLevel = value['stats']['rFlatEnergyModPerLevel'] if 'rFlatEnergyModPerLevel' in value['stats'] else 0
            existing_item.PercentLifeStealMod = value['stats']['PercentLifeStealMod'] if 'PercentLifeStealMod' in value['stats'] else 0
            existing_item.PercentSpellVampMod = value['stats']['PercentSpellVampMod'] if 'PercentSpellVampMod' in value['stats'] else 0

            if 'into' in value:
                for into_item in value['into']:
                    existing_into_item = Item.objects.filter(itemId=into_item)
                    if existing_into_item.count() == 0:
                        existing_into_item = Item(
                            itemId=into_item,
                        )
                        existing_into_item.save()
                    else:
                        existing_into_item = Item.objects.get(itemId=into_item)

                    if existing_into_item not in existing_item.built_into.all():
                        existing_item.built_into.add(existing_into_item)

            if 'from' in value:
                for from_item in value['from']:
                    existing_from_item = Item.objects.filter(itemId=from_item)
                    if existing_from_item.count() == 0:
                        existing_from_item = Item(
                            itemId=from_item,
                        )
                        existing_from_item.save()
                    else:
                        existing_from_item = Item.objects.get(itemId=from_item)

                    if existing_from_item not in existing_item.built_from.all():
                        existing_item.built_from.add(existing_from_item)

            existing_item.save()

            print(Fore.YELLOW + 'Item updated: ' + Style.RESET_ALL + existing_item.name)

        else:
            print(Fore.CYAN + 'Item already up to date: ' + Style.RESET_ALL + existing_item.name)


def check_summoner_spells(version):  # Create/Update all summoner spells.
    summoner_spell_info = fetch_ddragon_api(version, 'data', 'summoner.json')
    for spell, value in summoner_spell_info['data'].items():
        existing_spell = SummonerSpell.objects.filter(key=value['key'])
        if existing_spell.count() == 0:
            existing_spell = SummonerSpell(key=value['key'])
            existing_spell.save()

            print(Fore.GREEN + 'New spell added: ' + Style.RESET_ALL + value['name'])

        existing_spell = SummonerSpell.objects.get(key=value['key'])

        if existing_spell.version != version:
            existing_spell.version = version
            existing_spell.key = value['key']
            existing_spell.summonerSpellId = value['id']
            existing_spell.name = value['name']
            existing_spell.description = value['description']
            existing_spell.tooltip = value['tooltip']
            existing_spell.maxrank = value['maxrank']
            existing_spell.cooldownBurn = value['cooldownBurn']
            existing_spell.costBurn = value['costBurn']
            existing_spell.summonerLevel = value['summonerLevel']
            existing_spell.costType = value['costType']
            existing_spell.maxammo = value['maxammo']
            existing_spell.rangeBurn = value['rangeBurn']
            existing_spell.image_full = value['image']['full']
            existing_spell.image_sprite = value['image']['sprite']
            existing_spell.image_group = value['image']['group']
            existing_spell.image_x = value['image']['x']
            existing_spell.image_y = value['image']['y']
            existing_spell.image_w = value['image']['w']
            existing_spell.image_h = value['image']['h']
            existing_spell.resource = value['resource'] if 'resource' in value else None

            for cooldown in value['cooldown']:
                existing_spell.cooldown = cooldown

            for cost in value['cost']:
                existing_spell.cost = cost

            for range in value['range']:
                existing_spell.range = range

            existing_spell.save()

            print(Fore.YELLOW + 'Spell updated: ' + Style.RESET_ALL + existing_spell.name)

        else:
            print(Fore.CYAN + 'Spell already up to date: ' + Style.RESET_ALL + existing_spell.name)


def check_ranked_tiers():  # Create Ranked tiers if they don't exist.

    # - Challenger
    existing_challenger = RankedTier.objects.filter(key='CHALLENGER')
    if existing_challenger.count() == 0:
        RankedTier.objects.create(
            key='CHALLENGER',
            name='Challenger',
            order=1,
        )

    # - Grandmaster
    existing_grandmaster = RankedTier.objects.filter(key='GRANDMASTER')
    if existing_grandmaster.count() == 0:
        RankedTier.objects.create(
            key='GRANDMASTER',
            name='Grandmaster',
            order=2,
        )

    # - Master
    existing_master = RankedTier.objects.filter(key='MASTER')
    if existing_master.count() == 0:
        RankedTier.objects.create(
            key='MASTER',
            name='Master',
            order=3,
        )

    # - Diamond
    existing_diamond = RankedTier.objects.filter(key='DIAMOND')
    if existing_diamond.count() == 0:
        RankedTier.objects.create(
            key='DIAMOND',
            name='Diamond',
            order=4,
        )

    # - Platinum
    existing_platinum = RankedTier.objects.filter(key='PLATINUM')
    if existing_platinum.count() == 0:
        RankedTier.objects.create(
            key='PLATINUM',
            name='Platinum',
            order=5,
        )

    # - Gold
    existing_gold = RankedTier.objects.filter(key='GOLD')
    if existing_gold.count() == 0:
        RankedTier.objects.create(
            key='GOLD',
            name='Gold',
            order=6,
        )

    # - Silver
    existing_silver = RankedTier.objects.filter(key='SILVER')
    if existing_silver.count() == 0:
        RankedTier.objects.create(
            key='SILVER',
            name='Silver',
            order=7,
        )

    # - Bronze
    existing_bronze = RankedTier.objects.filter(key='BRONZE')
    if existing_bronze.count() == 0:
        RankedTier.objects.create(
            key='BRONZE',
            name='Bronze',
            order=8,
        )

    # - Iron
    existing_iron = RankedTier.objects.filter(key='IRON')
    if existing_iron.count() == 0:
        RankedTier.objects.create(
            key='IRON',
            name='Iron',
            order=9,
        )
