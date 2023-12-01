import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict

print("--- Day 14: Extended Polymerization ---")
#### Main
start_time = datetime.now()

def polymerizeFast(letters, pairs, rules):
    newPairs = {}
    for pair, nb in pairs.items():
        newOnes = [pair[0] + rules[pair], rules[pair] + pair[1]]
        for new in newOnes:
            if new in newPairs:
                newPairs[new] += nb
            else:
                newPairs[new] = nb
        letters[rules[pair]] += nb
    return(letters, newPairs)

rules = {}
f = open(".\Day14.txt", "r")
i = 0
for line in f:
    if i == 0:
        startPol = line.rstrip()
    elif i >= 2:
        input = line.rstrip().split(' -> ')
        rules[input[0]] = input[1]
    i += 1
f.close()

pairs = defaultdict(lambda: 0)
letters = defaultdict(lambda: 0)

## initialising letter count
for c in startPol:
    letters[c] += 1

## initialising pairs
for i in range(len(startPol) - 1):
    pair = startPol[i] + startPol[i + 1]
    pairs[pair] += 1

for i in range(40):
    letters, pairs = polymerizeFast(letters, pairs, rules)
    if i == 9:
        print(f"** Second Star : {max(letters.values()) - min(letters.values())}")
print(f"** Second Star : {max(letters.values()) - min(letters.values())}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))