from dice import roll_dice as dice
import random

class Battle:
    def __init__(self, _creatures):
        self.turn_count = 1
        self.teams = []
        self.creatures = []
        self.teamsform(_creatures)
        # the code above create:

        
            
        self.creatures.sort(key=lambda creatures: creatures.iniciative, reverse = True)



    def teamsform(self, _creatures):
        result = []
        times = _creatures
        for index, time in enumerate(times):
            nameteam = chr(65 + index)
            timeList = {"name": nameteam, "creatures": []}
            for creature in time:
                creature.team = nameteam  # return char like 'a' to differentiate the teams
                creature.iniciative = creature.iniciative_roll() ## iniciative init
                timeList["creatures"].append(creature.name)
            result.append(timeList)

        self.teams = result
        self.creatures = [c for team in times for c in team]



    # creatureteam = creature.team
    def choiceTarget(self, creatureteam):
        teamchosen = [team['name'] for team in self.teams if team['name'] != creatureteam]
        _creatures = [creature for creature in self.creatures if creature.team in teamchosen]
        target = random.choice(_creatures)
        
        return target

    def turnCreature(self, creature):
        if creature.is_alive():
            target = self.choiceTarget(creature.team)
            damage_attack = creature.actions[0].attack(target)
            if damage_attack[0] != "0d0":
                target.takesDamage(damage_attack[0][1])
                print(f"{creature.name} atacou o {target.name} esta com {target.HP} de pontos de vida")
            else:
                print("errou")
        else:
            print(f"{creature.name} esta morto")

    
    def start(self):
        self.turns = 1
        while self.turns <= 10:
            for creature in self.creatures:
                self.turnCreature(creature)
            self.turns += 1

