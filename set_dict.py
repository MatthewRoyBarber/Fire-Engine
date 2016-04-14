# locals() makes a dictionary of every parameter name as a key to the passed in values

def growth_stats(health, damage, skill, speed, luck, defence, resitance):
    return locals()

def fixed_stats(move, constitution, aid, travel, affinity, status):
    return locals()

def melee_weapon_ranks(swords, spears, axes, bows):
    return locals()

def magic_weapon_ranks(anima, light, dark, staves):
    return locals()

def growth_rates(health, damage, skill, speed, luck, defence, resitance):
    return locals()

def inventory(a, b, c, d, e):
    return {'1': a, '2': b, '3': c, '4': d, '5': e}

def weapon_stats(weapon_type, rank, might, range_min, range_max, hit, weight, critical):
    return locals()
