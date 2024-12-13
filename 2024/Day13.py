from datetime import datetime
from collections import defaultdict
import re
import math

#### Main
print(f"2024 --- Day 13: Claw Contraption ---")
start_time = datetime.now()

regexp = "X.(?P<X>\d+), Y.(?P<Y>\d+)"

def readInstruction(file):
    f = open(file, "r")
    instructions = {}
    ## read all instruction : 

    ClawID = 0
    instructions[ClawID] = []
    for i,line in enumerate(f):
        line = line.rstrip()
        if (i+1)%4 == 0:
            ClawID += 1
            instructions[ClawID] = []
        else:
            matches = re.finditer(regexp, line)
            for match in matches:
                instructions[ClawID].append([int(match.group('X')), int(match.group('Y'))])
    return(instructions)

def getPush(machine):
    button_A = machine[0]
    button_B = machine[1]
    target = machine[2]
    
    ## resolution du systeme de 2 equations à 2 inconnnus
    # xt = na*xa + nb*xb
    # yt = na*Ya + nb*yb
    # na = (xt-nb*xb)/xa
    # nb = (yt*xa - xt*ya) / (yb*xa - xb*ya)
    # solution si nb et na sont entiers, on test au 3eme digit

    push_b = (target[1]*button_A[0] - target[0]*button_A[1]) / (button_B[1] * button_A[0] - button_B[0]*button_A[1])

    if int(push_b*1000) != round(push_b,0)*1000:
        #print(f"machine {machine} - push_b={push_b} --> pas entier, on quitte")
        return(None)
    push_b = int(push_b)

    push_a = (target[0]-push_b*button_B[0])/button_A[0]
    if int(push_a*1000) != round(push_a,0)*1000:
        #print(f"machine {machine} - push_a={push_a} --> pas entier, on quitte")
        return(None)

    return(int(push_a), int(push_b))

def stars(instructions):
    star1 = 0
    star2 = 0

    for machineID, machine in instructions.items():
        result = getPush(machine)
        #print(f"Machine {machineID} -> {result}")
        if result != None:
            star1 += result[0] * 3 + result[1]
        
        machine[2][0] += 10000000000000
        machine[2][1] += 10000000000000

        result = getPush(machine)
        #print(f"Machine {machineID} -> {result}")
        if result != None:
            star2 += result[0] * 3 + result[1]

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day13.txt"

instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 