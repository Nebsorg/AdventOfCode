import copy
import math
import statistics
from datetime import datetime
from collections import defaultdict

print("--- Day 13: Transparent Origami ---")

#### Main
start_time = datetime.now()

def printDots(dots):
    sizeX = max([v[0] for v in dots]) + 1
    sizeY = max([v[1] for v in dots]) + 1

    for y in range(sizeY):
        line = ''
        for x in range(sizeX):
            if [x,y] in dots:
                line+='#'
            else:
                line+=' '
        print(line)

def foldX(dots, XFold):
    result = []
    for dot in dots:
        if dot[0] > XFold:
            newDot = [(XFold * 2) - dot[0], dot[1]]
        else:
            newDot = [dot[0], dot[1]]
        if newDot not in result:
            result.append(newDot)
    return(result)

def foldY(dots, YFold):
    result = []
    for dot in dots:
        if dot[1] > YFold:
            newDot = [dot[0], (YFold * 2) - dot[1]]
        else:
            newDot = [dot[0], dot[1]]
        if newDot not in result:
            result.append(newDot)
    return(result)

dots = []
foldInstruction = []
f = open(".\Day13.txt", "r")
for line in f:
    line = line.rstrip()
    if line != '':
        input = line.split(',')
        if len(input) == 2:
            dots.append([int(input[0]), int(input[1])])
        else:
            input = line.split('=')
            foldInstruction.append((input[0][-1], int(input[1])))

f.close()

for i, instruction in enumerate(foldInstruction):
   if instruction[0] == 'x':
        dots = foldX(dots, instruction[1])
   else:
       dots = foldY(dots, instruction[1])
   if i == 0:
       print(f"** First Star = {len(dots)}")

print(f"** Second Star : ")
printDots(dots)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))