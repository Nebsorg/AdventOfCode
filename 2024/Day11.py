from datetime import datetime
from collections import defaultdict
import copy

#### Main
print(f"2024 --- Day 11: Plutonian Pebbles ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    instructions = []
    stones = {}
    ## read all instruction : 

    for i,line in enumerate(f):
        line = line.rstrip()
        for val in line.split(" "):
            stones[int(val)] = 1
    
    return([stones])


def applyRule(stoneId):
    stoneId_str = str(stoneId)
    if stoneId == 0:
        return([1])
    elif len(stoneId_str) % 2 == 0:
        mid = len(stoneId_str)//2
        return([int(stoneId_str[:mid]), int(stoneId_str[mid:])])
    else:
        return([stoneId*2024])

def blink(stones):
    new_stones = defaultdict(lambda: 0)
    for stoneId in stones.keys():
        occurence = stones[stoneId]
        if occurence > 0:
            newIds = applyRule(stoneId)
            for newId in newIds:
                new_stones[newId] += occurence
    return(new_stones)

def stars(instructions):
    star1 = 0
    star2 = 0

    stones = instructions[0]

    for i in range(75):
        stones = blink(stones)
        if i == 24:
            star1 = sum(stones.values())
    star2 = sum(stones.values())

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day11.txt"
instructions = readInstruction(fileToOpen)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 