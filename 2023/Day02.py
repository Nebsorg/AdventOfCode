from datetime import datetime
import re
import math

#### Main
print("2023 --- Day 2: Cube Conundrum ---")
start_time = datetime.now()

regExp = "((?P<w_color_quantity>(\d*)) (?P<w_color>(red|blue|green))(,?))+"


fileToOpen = "./2023/Day02.txt"

f = open(fileToOpen, "r")
maxCubes = {'red': 12, 'green': 13, 'blue': 14}

sumPossible = 0
sumPower = 0
for line in f:
    line = line.rstrip()

    game_ID = int(line.split(':')[0].split(' ')[1])
    game_sets = line.split(':')[1].split(';')

    impossible = False
    minCubes = {'red': 0, 'green': 0, 'blue': 0}

    for game_set in game_sets: 
        matches = re.finditer(regExp, game_set)
        for match in matches:
            color = match.group('w_color')
            qty = int(match.group('w_color_quantity'))
            
            ## First Star : check max qty
            if qty > maxCubes[color]: 
                #print(f"Game {game_ID} Impossible - color {color} exeed max quantity {qty} > {maxCubes[color]}")
                impossible = True

            ## Second Star : keep min per color
            minCubes[color] = max(minCubes[color], qty)

    if not impossible:
        sumPossible += game_ID

    sumPower += math.prod(minCubes.values())
    #print(f"Game {game_ID} - Power={gamePower}")

print(f"****** First Star = {sumPossible}")
print(f"****** Second Star = {sumPower}")


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 