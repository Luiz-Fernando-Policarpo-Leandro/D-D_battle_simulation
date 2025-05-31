from dice import roll_dice as dice
import random

class Battle:
    def __init__(self, _creatures):
        self.turn_count = 1
        self.teamsform(_creatures)
        # the code above create:
            # self.teams
            # self.creatures
        self.creatures.sort(key=lambda creatures: creatures.iniciative, reverse = True)

        ##  start
        #self.start()


    def teamsform(self, _creatures):
        result = []
        times = _creatures
        for index, time in enumerate(times):
            nameteam = chr(65 + index)
            timeList = {"name": nameteam, "creatures": []}
            for creature in time:
                creature.team = nameteam  # return char like 'a' to differentiate the teams
                creature.HP = creature.PV
                creature.iniciative = dice(f"1d20+{creature.attribute['dex']['modifier']}")[1] ## iniciative init
                timeList["creatures"].append(creature.name)
            result.append(timeList)

        self.teams = result
        self.creatures = [c for team in times for c in team]


    def choisetarget(self, creatureteam):
        teamchosen = [team['name'] for team in self.teams if team['name'] != creatureteam.team]
        creatures = [(c.name, c.team)  for c in self.creatures if c.team in teamchosen]
        target = random.choice(creatures)

        return target 



    def turn(self, creature):
        if creature.HP > 0:
            #chosetarget = random
            pass
    
    def start(self):
        self.turn = 1
        while True:
            for creature in self.creature:
                self.turn(creature)
            break