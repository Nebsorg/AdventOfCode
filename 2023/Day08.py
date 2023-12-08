from datetime import datetime
import math
from functools import reduce
import re

#### Main
print("2023 --- Day 8: Haunted Wasteland ---")
start_time = datetime.now()

def readInstruction(file):
    regexp = "(?P<w_start>(\w{3})) = \((?P<w_left>(\w{3})), (?P<w_right>(\w{3}))\)"
    f = open(file, "r")
    ## read all instruction : 
    map = {}
    for i, line in enumerate(f):
        line = line.rstrip()

        if i == 0:
            instructions = line

        if i >= 2:
            matches = re.finditer(regexp, line)
            for match in matches:
                src = match.group("w_start")
                dest = [match.group("w_left"), match.group("w_right")]
                map[src] = dest
    return(instructions, map)

def computeCycle(instructions, map, start_node):
    current_node = start_node
    current_instruction = 0
    steps = 0
    
    cycleComplete = False
    while not cycleComplete:
        direction = instructions[current_instruction]
        if direction == 'R':
            next_node = map[current_node][1]
        else:
            next_node = map[current_node][0]

        current_instruction += 1
        if current_instruction >= len(instructions):
            current_instruction = 0
        steps += 1

        if next_node[2] == 'Z':
            cycleComplete = True
        current_node = next_node
    return(steps)


def Firststar(instructions, map):
    result = computeCycle(instructions, map, 'AAA')
    print(f"****** First Star = {result}")

def SecondStar(instructions, map):
    starting_nodes = [d for d in map.keys() if d[2] == 'A']

    steps = []
    for node in starting_nodes:
        result = computeCycle(instructions, map, node)
        steps.append(result)

    result = reduce(lambda a,b:math.lcm(a,b), steps)
    print(f"****** Second Star = {result}")

fileToOpen = "./2023/Day08.txt"
instructions, map = readInstruction(fileToOpen)

Firststar(instructions, map)
SecondStar(instructions, map)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 