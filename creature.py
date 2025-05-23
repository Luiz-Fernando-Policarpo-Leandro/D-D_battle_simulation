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
        self.parent = parent  # Referência à criatura dona da ação
    
    def attack(self,cd):
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
                damage = damage if resroll == 'saved' else (str(int(damage[0]) * 2)  + damage[1:])
                return damage, resroll
            return "0d0", resroll
                




class Creature:
    def __init__(self, name, _type, size, alignment, ac, ac_type, pv,
                 attributes, skills, resistance, vulnerability, immunity,
                 languages, cd, especial, spell, actions):

        self.name = name
        self.type = _type
        self.size = size
        self.alignment = alignment

        self.AC = ac
        self.AcType = ac_type
        self.PV = pv
        self.attributes = attributes
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