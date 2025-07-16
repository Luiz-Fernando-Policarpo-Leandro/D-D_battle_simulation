from dice import roll_dice as dice, checkTest

class Actions:
    def __init__(self, data, parent=None):
        self.name = data.get("name")
        self.type_action = data.get("type_action", [])
        self.multiAtk = data.get("multiAtk", [])
        self.damage = data.get("damage", [])
        self.target = data.get("target", [])
        self.bonus = data.get("bonus", 0)
        self.cd = data.get("cd", 0)
        self.parent = parent  # reference of the owner creature
    
    def attack(self,creature):
        cd = creature.AC
        if self.multiAtk:
            results = []
            sum_result = 0
            for atk_name in self.multiAtk:
                for action in self.parent.actions:
                    if action.name == atk_name:
                        atk = action.attack(cd)
                        results.append((atk_name, atk))
                        sum_result += atk[1] if isinstance(atk, int) else 0
                        break
            return results, sum_result
        elif self.damage:
            resroll = checkTest(cd, self.bonus)[1]
            damage = self.damage[1]
            if resroll in ['critical save', 'saved']:
                damage = dice(damage if resroll == 'saved' else (str(int(damage[0]) * 2)  + damage[1:]))
                # return ((...dices, sum[dices]), rsultu)
                return damage, resroll 
            return "0d0", resroll
                
def attributesForm(attrs):
    def form(score):
        return {"value": score , "modifier":((score-10) // 2)}
    
    result = {}
    for name, value in attrs.items():
        result[name.lower()] = form(value)
    return result
    


class Creature:
    def __init__(self, name, _type, size, alignment, ac, ac_type, HP,
                 attributes, skills, resistance, vulnerability, immunity,
                 languages, cd, especial, spell, actions):

        self.name = name
        self.type = _type
        self.size = size
        self.alignment = alignment

        self.AC = ac
        self.AcType = ac_type
        
        self.MAXIMUM_HP = HP # maximum hit points
        self.HP = HP #hit points
        self.TEMPORARY_HP = 0 # temporary hit points
        self.death_checks = {'save': 0, 'failed': 0}


        # creature.attribute['dex']['modifier'] || ['value']
        self.attribute = attributesForm(attributes) 
        self.skills = skills

        self.resistance = resistance
        self.vulnerability = vulnerability
        self.immunity = immunity

        self.languages = languages

        self.CD = cd
        self.especial = especial
        self.spell = spell

        self.actions = []
        if actions:
            for act in actions:
                self.actions.append(Actions(act, parent=self))

    def iniciative_roll(self):
	    return dice(f"1d20 + {self.attribute["dex"]["modifier"]}")[1]

    def healing(self,cure):
        # if the creature is prone
        if self.HP < 0:
            self.HP = cure
            self.deathCheck("alive")
        # checks if the cure is higher more than the maximum HP
        if (self.HP + cure) > self.MAXIMUM_HP:
            self.HP = self.MAXIMUM_HP
        
        
    def is_alive(self):
        return self.HP > 0

    def deathCheck(self, result_check = 0):
        if result_check > 0:
            self.death_checks['save'] += 1
        if result_check < 0:
            self.death_checks['failed'] += 1


    def takesDamage(self, damageHit):
        if damageHit < 0: # Certifique-se de que o dano é positivo
            damageHit = 0

        # Primeiro, aplique o dano ao HP Temporário
        if self.TEMPORARY_HP > 0:
            if damageHit <= self.TEMPORARY_HP:
                self.TEMPORARY_HP -= damageHit
                damageHit = 0 # Todo o dano foi absorvido pelo HP temporário
            else:
                damageHit -= self.TEMPORARY_HP
                self.TEMPORARY_HP = 0

        # Em seguida, aplique o dano restante ao HP real
        if damageHit > 0:
            self.HP -= damageHit

        # Verifique se a criatura ainda está viva e atualize o status de morte
        if self.HP <= 0:
            self.HP = 0 # Garante que o HP não seja negativo
            if self.is_alive(): # Se era viva e agora não é mais
                self.is_alive = False # Você pode adicionar um atributo is_alive no __init__
                self.deathCheck(-1) # Ou chame isso apenas uma vez ao morrer
                print(f"{self.name} foi derrotado!")
