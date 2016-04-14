from include import *

class Unit:
    
    def __init__(self, name, description, level, experience, unit_class, growth_stats, fixed_stats, ranks, growth_rates, inventory):
        self.name = name
        self.description = description
        self.level = level
        self.base_level = self.level
        self.experience = experience
        self.unit_class = unit_class
        self.growth_stats = growth_stats
        self.fixed_stats = fixed_stats
        self.current_health = self.growth_stats['health']
        self.ranks = ranks
        self.growth_rates = growth_rates
        self.inventory = inventory
        self.increase_log = []
        
    # Actions

    def update_exp(self, exp_gain):
        current_exp = exp_gain + self.experience
        if(current_exp >= 100):
            for x in range(current_exp // 100):
                self.level_up()
                self.experience = current_exp - 100
        else:
            self.experience = current_exp

    def level_up(self):
        self.level += 1
        for stat in GROWTH_STATS:
            rate = self.growth_rates[stat]
            rand = random.randint(0, 100)
            if rand < rate:
                should_increase = True
            else:
                should_increase = False
            self.increase_log[self.level] = {stat: should_increase}

    # Getters

    def get_stat(self, stat):
        if(stat in GROWTH_STATS):
            value = self.growth_stats[stat]
            for x in range((self.base_level + 1), self.level):
                if(self.increase_log[x][stat]):
                    value += 1
            return value
        else:
            return self.fixed_stats[stat]

    """
    def get_weapon_rank(self, weapon_rank):
        rank = '0';
        if
    """

    def get_attack_speed(self, weapon_weight):
        constitution = self.fixed_stats['constitution']
        speed = self.get_stat('speed')
        if(weapon_weight <= constitution):
            return speed
        else:
            return speed - (weapon_weight - constitution)

    def get_hit_rate(self, weapon_accuracy):
        return weapon_accuracy + (self.get_stat('skill') * 2) + int(self.get_stat('luck') / 2)

    def get_attack_power(self, weapon_might, triangle_bonus, weapon_effectiveness):
        return self.get_stat('damage') + (weapon_might + triangle_bonus) * weapon_effectiveness

    def get_defence_power(self, terrain_bonus, attack_type):
        defence_rating = 0
        if(attack_type == 'M'):
           defence_rating = self.get_stat('resistance')
        if(attack_type == 'S'):
           defence_rating = self.get_stat('defence')
        return defence_rating + terrain_bonus

    def get_critical_rate(self, weapon_critical):
        # Need to add class critical bonus into the equation
        return weapon_critical + int(self.get_stat('skill') / 2)

    def get_critical_chance(self, critical_rate):
        return critical_rate - self.get_stat('luck')

Bob = Unit("Bob", "A humble builder",
                10, 50, 'cavalier',
                set_dict.growth_stats(20, 10, 10, 10, 10, 10, 10),
                set_dict.fixed_stats(5, 7, 6, '', 'anima', ''),
                set_dict.melee_weapon_ranks('71', '121', '0', '0'),
                set_dict.growth_rates(80, 40, 40, 50, 40, 25, 20),
                set_dict.inventory('', '', '', '', ''))

