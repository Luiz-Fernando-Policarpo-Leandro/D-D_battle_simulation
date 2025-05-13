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
    
    def attack(self):
        if self.multiAtk:
            results = []
            sum_result = 0
            for atk_name in self.multiAtk:
                for action in self.parent.actions:
                    if action.name == atk_name:
                        atk = action.attack()
                        results.append((atk_name, atk))
                        sum_result += atk[1]
                        break
            return results, sum_result
        elif self.damage:
            return dice(self.damage[1])


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



add = {
    "name": "Giant Ape",
    "_type": "Beast",
    "size": "Huge",
    "alignment": "Unaligned",
    "ac": 12,
    "ac_type": "natural armor",
    "pv": 157,
    "attributes": {
        "STR": 23,
        "DEX": 14,
        "CON": 18,
        "INT": 7,
        "WIS": 12,
        "CHA": 7
    },
    "skills": {"Athletics": 9, "Perception": 4},
    "resistance": [],
    "vulnerability": [],
    "immunity": [],
    "languages": [],
    "cd": 7,
    "especial": None,
    "spell": [],
    "actions": [
        {
            "name": "Fist",
            "type_action": ["action", "Melee Weapon Attack"],
            "damage": [1, "3d10+6", "bludgeoning"],
            "target": ["one target", "3 m"],
            "bonus": 9
        },
        {
            "name": "Rock",
            "type_action": ["action", "Ranged Weapon Attack"],
            "damage": [1, "7d6+6", "bludgeoning"],
            "target": ["one target", "15/30 m"]
        },
        {
            "name": "Multiattack",
            "multiAtk": ["Fist", "Fist"]
        }
    ]
}

x = Creature(**add)

# //x.actions.attack()