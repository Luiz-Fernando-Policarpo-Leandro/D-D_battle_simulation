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
    
    def attack(self, creature):
        cd = creature.AC
        if self.multiAtk:
            results = []
            sum_result = 0
            for atk_name in self.multiAtk:
                for action in self.parent.actions:
                    if action.name == atk_name:
                        atk = action.attack(creature)
                        results.append((atk_name, atk))
                        if isinstance(atk, tuple):
                            sum_result += atk[1]
                        break
            return results, sum_result

        elif self.damage:
            resroll = checkTest(cd, self.bonus)[1]
            damage = self.damage[1]

            if resroll not in ['critical save', 'saved']:
                return "0d0", resroll

            qtd, rest = damage.split("d", 1)
            damage = damage if resroll == 'saved' else f"{int(qtd) * 2}d{rest}"

            damage = dice(damage)
            return damage, resroll


                
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
        self.death_checks = {'saved': 0, 'failed': 0}
        self.status_creature = "alive"


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
	    return dice(f"1d20 + {self.attribute['dex']['modifier']}")[1]



    def is_alive(self):
        return self.HP > 0 and self.status_creature != "dead"

    def deathCheck(self, result_check = "saved", damage = 0):
        """
        This method make the death checks
        - check if stable or takes damage
        - check if damage is higher than MAX_HITPOINTS
        - check if result_check is a failed or a save
        - if failed acressent 1 in death
        - if saved acressent 1 in save
        - if death_checks is higher morer 2, so status is updated
        """

        if self.status_creature == "stable" and not damage:
            return

        if damage >= self.MAXIMUM_HP:
            self.status_creature = "dead"
            return

        if result_check == "failed" or damage:
            self.death_checks['failed'] += 1
            if self.death_checks['failed'] > 2:
                self.status_creature = "dead"
            return

        self.death_checks['saved'] += 1

        if self.death_checks['saved'] > 2:
            self.status_creature = "stable"



    def healing(self,cure = 1):

        """
        this method cure the creature
        - checks if creature HITPOINTS IS higher more MAX_HITPOINTS
        """
        if self.HP == self.MAXIMUM_HP:
            return

        if not self.is_alive():  # estava caída
            self.HP = cure
            self.death_checks = {'saved': 0, 'failed': 0}
            self.status_creature = "alive"
        else:
            self.HP = min(self.HP + cure, self.MAXIMUM_HP)




    def takesDamage(self, damageHit):
        """
        This method applies damage and reduces it if necessary:
        - first check if alive, else make the deathchecks
        - return if there's no damage
        - reduce damage using TEMPORARY_HP if available
        - reduce actual HP
        - set status to 'unconscious' if HP drops to 0
        """
        if self.is_alive():

            if damageHit < 1:
                damageHit = 0
                return

            if self.TEMPORARY_HP > 0:
                if damageHit <= self.TEMPORARY_HP:
                    self.TEMPORARY_HP -= damageHit
                    return
                damageHit -= self.TEMPORARY_HP
                self.TEMPORARY_HP = 0


            if damageHit > 0:
                self.HP -= damageHit
                self.HP = max(self.HP, 0)

            if self.HP <= 0 and self.status_creature == "alive":
                self.status_creature = "unconscious"

        else:
            self.HP = 0
            self.deathCheck("failed",damageHit)


if __name__ == "__main__":
    pass
