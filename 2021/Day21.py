import copy
import math
from datetime import datetime
import re
from ast import literal_eval

print("--- Day 21: Dirac Dice ---")
reg_list = "\[(?P<left>\d*),(?P<right>\d*)\]"
#### Main
start_time = datetime.now()


def displayPicture(picture):
    for line in picture:
        print(''.join(line))

def rollDiceDeterministic(dice):
    dice += 1
    if dice == 101:
        return(1)
    else:
        return(dice)

def star1(playersPosition):
    scores = [0,0]
    dice = 0
    currentPlayer = 0
    iteration = 0

    while max(scores) < 1000:
        ## currentRoad player roll dice
        move = 0
        for i in range(3):
            dice = rollDiceDeterministic(dice)
            move += dice

        print(f"Tour {iteration} - score = {scores} - current player = {currentPlayer + 1} - position={playersPosition[currentPlayer]}")
        playersPosition[currentPlayer] = (((playersPosition[currentPlayer] + move)-1)%10)+1
        scores[currentPlayer] += playersPosition[currentPlayer]
        print(f"   - move={move} - new position={playersPosition[currentPlayer]} - new score = {scores}")
        ## change player:
        if currentPlayer == 0:
            currentPlayer = 1
        else:
            currentPlayer = 0
        iteration += 1

    print(f"** Star1: {min(scores)*3*iteration} - numberof time={iteration, 3*iteration}")




f = open(".\Day21.txt", "r")
lineID = 0
playersPosition = []
for line in f:
    if lineID == 0:
        playersPosition.append(int(line.rstrip()[28:30]))
    elif lineID ==1:
        playersPosition.append(int(line.rstrip()[28]))
    lineID += 1
f.close()

print(f"{playersPosition}")
star1(playersPosition)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))