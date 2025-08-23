import random

class Dice:
    def __init__(self, type_dice, min_value = 1):
        self.min_value = min_value
        self.type_dice = type_dice
    
    def roller(self):
        return random.randint(self.min_value, self.type_dice)
    

def roll_dice(dice_str):
    try:
        parts = dice_str.split('d') # if the string is '2d20' the array is [2,20] 
        num_dice = int(parts[0]) # number of dices
        sum_dice = 0 #sum of the dice operator
        

        # check if there any sum, '2d20+5' after split part, return [2, 20+5]
        opCheck = parts[1]
        operator = '+' if '+' in opCheck else '-' if '-' in opCheck else ''
        mult = (1 if '+' in operator else -1)


        # verify if there any operator
        if operator:
            dice_type, sum_dice = map(int,parts[1].split(operator))
            sum_dice = sum_dice * mult
        else:
            dice_type = int(opCheck) 
        
        # create dice object
        dice = Dice(dice_type) 

        #roll the dices in agroup in array
        result = [dice.roller() for _ in range(num_dice)]
        total = sum(result) + sum_dice

        # return [...dices, sum(total)]
        return result, total if total > 1 else 1
    
    except Exception as error:
        return f"Erro no '{dice_str}': {error}"


def advantage_roll(advantage,dices):
    return max(dices) if advantage == "advantage" else min(dices)


## commner testes

def checkTest(cd, bonus, roll_with=''):
    result_dice, _ = roll_dice(f"{2 if roll_with else 1}d20")
    
    if roll_with:
        final_dice_result = advantage_roll(roll_with,result_dice)
    else:
        final_dice_result = result_dice[0]
    
    final = final_dice_result + bonus

    if (final) > cd or final_dice_result == 20:
        result_test = "saved" if final_dice_result != 20 else "critical save"
    else:
        result_test = "failure" if final_dice_result != 1 else "critical failure"
    
    return final_dice_result, result_test , final


if __name__ == "__main__":
    pass
