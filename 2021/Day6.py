import copy
from datetime import datetime
from collections import defaultdict

print("--- Day 6: Lanternfish ---")

def naissance(couveuse, numberOfDays, caption):

    for i in range(numberOfDays):
        newFish = couveuse[0]
        for day in range(8):
            couveuse[day] = couveuse[day+1]
        couveuse[6] += newFish
        couveuse[8] = newFish

    numberOfFishs = sum(couveuse.values())
    print(f"  ** {caption} : Number of fish after {numberOfDays} days = {numberOfFishs}")
    return(numberOfFishs)

start_time = datetime.now()
instructions = defaultdict(lambda: 0)

f = open(".\Day6.txt", "r")
for line in f:
    instruction = line.rstrip().split(",")
    for v in instruction:
        instructions[int(v)] += 1
f.close()


couveuse = copy.deepcopy(instructions)
nbOfFish = naissance(couveuse, 80, "Star 1")

couveuse = copy.deepcopy(instructions)
nbOfFish = naissance(couveuse, 256, "Star 2")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))