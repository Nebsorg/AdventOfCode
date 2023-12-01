import copy
import math
from datetime import datetime
import re
from ast import literal_eval

print("--- Day 18: Snailfish ---")
reg_list = "\[(?P<left>\d*),(?P<right>\d*)\]"
#### Main
start_time = datetime.now()

def checkSplit(expression):
    match = re.search(r"\d{2}", expression)
    if match:
        position = match.start()
        number = int(match.group(0))
        sublist = '['+str(math.floor(number/2))+','+str(math.ceil(number/2))+']'
        result = expression[:position] + sublist + expression[position+2:]
        return(True, result)
    return(False, expression)


def checkExplosion(expression):
    depth = 0

    # print(f"**** checking Explosion for {expression}")
    for position,c in enumerate(expression):
        if c == '[':
            depth += 1
        elif c == ']':
            depth -= 1

        if depth >= 5:
            match = re.search(reg_list, expression[position:])
            values = [int(match.group('left')), int(match.group('right'))]
            pairPosition = match.start()+position
            explosionSize = len(match.group('left')) + len(match.group('right')) + 3
            break
    else:
        return(False,expression)

    ## Explosion happend

    result = ""
    ## Completing left part and incresing leftmost digit
    leftPart = expression[:pairPosition]
    # print(f"  - searching last digit to increment on the left {leftPart}")
    if re.search("\d+", leftPart) is not None:
        matchs = re.finditer("\d+", leftPart)
        *_, last = matchs
        intValue = int(leftPart[last.start(): last.end()])
        # print(f"  - left int {intValue} found on position {last.start(), last.end()} - increast it by {values[0]}")
        intValue += values[0]
        result += leftPart[:last.start()] + str(intValue) + leftPart[last.end():]

    else:
        result += leftPart
        # print(f"  - no int found on left")

    ## replacing current pair with 0
    result += '0'

    ## Completing right part and incresing rightmost digit
    rightPart = expression[pairPosition+explosionSize:]
    match = re.search("\d+", rightPart)
    if match:
        intValue = int(rightPart[match.start(): match.end()])
        intValue += values[1]
        result += rightPart[:match.start()] + str(intValue) + rightPart[match.end():]
    else:
        result += rightPart
    return(True, result)

def reduce(expression):
    onGoing = True
    result = expression
    while onGoing:
        onGoing = True
        isExploded, result = checkExplosion(result)
        if isExploded == False:
            isSplited, result = checkSplit(result)
            if isSplited == False:
                onGoing = False
    return(result)

def sumFish(fish1, fish2):
    newFish = '['+fish1+','+fish2+']'
    newFish = reduce(newFish)
    return(newFish)


def evalMagnitude(snailfish):
    if type(snailfish[0]) is list:
        leftvalue = evalMagnitude(snailfish[0])
    else:
        leftvalue = snailfish[0]

    if type(snailfish[1]) is list:
        rightvalue = evalMagnitude(snailfish[1])
    else:
        rightvalue = snailfish[1]

    return(leftvalue*3 + rightvalue*2)

def star1(fishlist):
    for lineID, fish in enumerate(fishlist):
        if lineID == 0:
            previousFish = fish
        else:
            currentFish = fish
            previousFish = sumFish(previousFish, currentFish)
    fish = literal_eval(previousFish)
    print(f"** First Star : {evalMagnitude(fish)}")

def star2(fishlist):
    max = 0
    for id1, fish1 in enumerate(fishlist):
        for id2, fish2 in enumerate(fishlist):
            if id1 != id2:
                # print(f"*** Summing fish {id1} - {fish1} and {id2} - {fish2}")
                newFish = sumFish(fish1, fish2)
                # print(f" - result = {newFish}")

                fish = literal_eval(newFish)
                magnitude = evalMagnitude(fish)
                if magnitude > max:
                    max = magnitude
    print(f"** Second Star (sum Max): {max}")

f = open(".\Day18.txt", "r")
fishList = []
for line in f:
    fishList.append(line.rstrip())
f.close()

star1(fishList)
star2(fishList)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))