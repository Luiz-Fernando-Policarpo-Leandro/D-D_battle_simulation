from dice import abilityModifier, roll_dice as dice

class Battle:
    def __init__(self, _creatures):
        self.turn_count = 1
        self.teamsform(_creatures)
        # the code above create:
            # self.teams
            # self.creatures
        self.creatures.sort(key=lambda creatures: creatures.iniciative, reverse = True)

        ##  start
        self.start()

    def iniciative_roll(self,dex):
        creatureDexMod = abilityModifier(dex)
        return dice(f"1d20+{creatureDexMod}")[1]


    def teamsform(self, _creatures):
        result = []
        times = _creatures
        for index, time in enumerate(times):
            nametime = chr(65 + index) if (len(time) > 1) else 'solo'
            timeList = {"name": nametime, "creatures": []}
            for creature in time:
                creature.time = nametime # return char like 'a' to differentiate the teams
                creature.HP = creature.PV
                creature.iniciative = self.iniciative_roll(creature.attributes["DEX"]) ## iniciative init
                timeList["creatures"].append(creature.name)
            result.append(timeList)

        self.teams = result
        self.creatures = sum(times, [])

    def turn(self, creature):
        if creature.HP > 0:
            pass
    
    def start(self):
        self.turn = 1
        while True:
            for creature in self.creature:
                self.turn(creature)
            break