import decimal
import math

claim1 = [30., 100., 40.]
claim2 = [15., 50., 70.]
winner_claim = [500., 101., 300., 600.]

MULTIPLIER = 3

loser_pot = sum(claim1) + sum(claim2)
remaining_pot = decimal.Decimal(0)
test_pot = decimal.Decimal(loser_pot)

winner_percentages = []
real_gains = []
for winner in winner_claim:
    percentage = float(decimal.Decimal(winner/sum(winner_claim))*decimal.Decimal(100))
    winner_percentages.append(percentage)

print(sum(winner_percentages))

def real_round(value):
    intvalue = value*1000
    intvalue = math.trunc(intvalue)
    if intvalue%10 < 5:
        tmp_value = math.trunc((intvalue)/10)
        return tmp_value/100
    else:
        tmp_value = math.trunc((intvalue + 10)/10)
        return tmp_value/100
    
for winner_index, winner in enumerate(winner_claim):
    potential_gain = (decimal.Decimal(winner_percentages[winner_index])/decimal.Decimal(100))*decimal.Decimal(loser_pot)
    if decimal.Decimal(winner)*MULTIPLIER < potential_gain:
        remainder = potential_gain - decimal.Decimal(winner)*MULTIPLIER
        remaining_pot += remainder
        real_gains.append(decimal.Decimal(winner)*MULTIPLIER)
    else:
        real_gains.append(potential_gain)

# Convert the remaining pot and real gains to two decimal places for display
#TODO: round down if under .005
remaining_pot = real_round(remaining_pot)
real_gains = [real_round(gain) for gain in real_gains]

print("Remaining Pot:", remaining_pot)
print("Real Gains:", real_gains)
print(sum(real_gains))