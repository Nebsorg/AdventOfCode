from datetime import datetime
from collections import defaultdict
from operator import mul
from functools import reduce
import copy
import re
import numpy as np

#### Main
print(f"2024 --- Day 14: Restroom Redoubt ---")
start_time = datetime.now()

regexp = "-?\d+"

def display(max_line, max_col, robot, boxes, walls):
    for i in range(max_line):
        line = ""
        for j in range(max_col):
            if [i,j] in boxes: line+='O'
            elif [i,j] == robot: line += '@'
            elif [i,j] in walls: line+='#'
            else: line+='.'
        print(line)

def display2(max_line, max_col, robot, boxes, walls):
    for i in range(max_line):
        line = ""
        j = 0
        while j < max_col:
            if [[i,j], [i, j+1]] in boxes.values(): 
                line+='[]'
                j+=2
            elif [i,j] == robot: 
                line += '@'
                j+=1
            elif [i,j] in walls: 
                line+='#'
                j+=1
            else: 
                line+='.'
                j+=1
        print(line)



def readInstructionStar1(file):
    f = open(file, "r")
    boxes = []
    walls = []
    directions = []
    max_row, max_col = 0, 0
    ## read all instruction : 
    reading = 0
    robot = [0,0]
    for i,line in enumerate(f):
        line = line.rstrip()
        if i == 0:
            max_col = len(line)
            for j in range(len(line)):
                walls.append([i,j])
        else:
            if reading == 0:
                ## on est dans la section carte
                if str(line[:5]) == "#####":
                    ## on est sur la fin de la section carte
                    reading = 1
                    max_row = i+1
                    for j in range(len(line)):
                        walls.append([i,j])
                else:
                    for j in range(len(line)):
                        if line[j] == 'O':
                            boxes.append([i,j])
                        elif line[j] == '@':
                            robot = [i,j]
                        elif line[j] == '#':
                            walls.append([i,j])
            else:
                for char in line:
                    match char:
                        case '<':
                            directions.append((0,-1))
                        case '>':
                            directions.append((0,1))
                        case '^':
                            directions.append((-1,0))
                        case 'v':
                            directions.append((1,0))
    return([(max_row, max_col), robot, boxes, walls, directions])

def readInstructionStar2(file):
    f = open(file, "r")
    boxes = {}
    walls = []
    directions = []
    max_row, max_col = 0, 0
    ## read all instruction : 
    reading = 0
    robot = [0,0]
    boxID = 0
    for i,line in enumerate(f):
        line = line.rstrip()
        if i == 0:
            max_col = 2*len(line)
            for j in range(len(line)):
                walls.extend([[i,2*j],[i, (2*j)+1]])
        else:
            if reading == 0:
                ## on est dans la section carte
                if str(line[:5]) == "#####":
                    ## on est sur la fin de la section carte
                    reading = 1
                    max_row = i+1
                    for j in range(len(line)):
                        walls.extend([[i,2*j],[i, (2*j)+1]])
                else:
                    pos = 0
                    for j in range(len(line)):
                        if line[j] == 'O':
                            boxes[boxID] = [[i,pos],[i, pos+1]]
                            boxID += 1
                        elif line[j] == '@':
                            robot = [i,pos]
                        elif line[j] == '#':
                            walls.extend([[i,pos],[i, pos+1]])
                        pos += 2
            else:
                for char in line:
                    match char:
                        case '<':
                            directions.append((0,-1))
                        case '>':
                            directions.append((0,1))
                        case '^':
                            directions.append((-1,0))
                        case 'v':
                            directions.append((1,0))
    return([(max_row, max_col), robot, boxes, walls, directions])




def moveRobot(robot, boxes, walls, direction):
    new_pos = [robot[0]+direction[0], robot[1] + direction[1]]
    encounteredBoxes = []
    
    finished = False
        
    while not finished:
        if new_pos in walls:
            #print(f"New pos dans un mur : {new_pos}")
            return

        if new_pos in boxes:
            ## on tombe dans une boite, est-ce qu'on peut la pousser ? 
            encounteredBoxes.append(boxes.index(new_pos))
            new_pos = [new_pos[0]+direction[0], new_pos[1] + direction[1]]
        else:
            ## on est ni dans un mur, ni dans un boite -> c'est vide, on peut se deplacer
            finished = True

    ## on deplace le robot et toutes les boites croisées
    robot[0] += direction[0]
    robot[1] += direction[1]
    for boxId in encounteredBoxes:
        boxes[boxId][0] += direction[0]
        boxes[boxId][1] += direction[1]


def moveRobot2(robot, boxes, walls, direction):
    occupied = {}
    for id, spaces in boxes.items():
        for pos in spaces:
            occupied[(pos[0], pos[1])] = id

    #print(boxes)
    #print(occupied)
    pos_to_check = [[robot[0]+direction[0], robot[1] + direction[1]]]
    encounteredBoxes = set()
    
    finished = False
        
    while len(pos_to_check) > 0:
        pos = pos_to_check.pop()
        if pos in walls:
            #print(f"New pos dans un mur : {pos}")
            return

        occupiedPos = tuple(pos)
        if occupiedPos in occupied.keys():
            ## on tombe dans une boite, est-ce qu'on peut la pousser ? 
            #print(f"on rencontre une boite en {pos} : ID={occupied[occupiedPos]} - value={boxes[occupied[occupiedPos]]}")

            encounteredBoxes.add(occupied[occupiedPos])
            if direction in [(1,0), (-1,0)]:
                ## deplacement verticale, il faut ajouter les deux elements de la caisse à tester
                for box_pos in boxes[occupied[occupiedPos]]:
                    pos_to_check.append([box_pos[0]+direction[0], box_pos[1] + direction[1]])
            else:
                ## deplacement horizontal
                pos_to_check.append([pos[0]+direction[0], pos[1] + direction[1]])
        else:
            ## on est ni dans un mur, ni dans un boite -> c'est vide, on peut se deplacer
            finished = True

    ## on deplace le robot et toutes les boites croisées
    robot[0] += direction[0]
    robot[1] += direction[1]
    for boxId in encounteredBoxes:
        #print(f"updating box {boxId} = {boxes[boxId]}")
        boxes[boxId][0][0] += direction[0]
        boxes[boxId][0][1] += direction[1]
        boxes[boxId][1][0] += direction[0]
        boxes[boxId][1][1] += direction[1]



def star1(fileToOpen):
    instructions = readInstructionStar1(fileToOpen)
    
    max_row = instructions[0][0]
    max_col = instructions[0][1]
    robot = copy.deepcopy(instructions[1])
    boxes = copy.deepcopy(instructions[2])
    walls = copy.deepcopy(instructions[3])
    directions = copy.deepcopy(instructions[4])

    display(max_row, max_col, robot, boxes, walls)
    while len(directions) > 0:
        direction = directions.pop(0)
        moveRobot(robot, boxes, walls, direction)
    
    star1 = sum([box[0]*100+box[1] for box in boxes])
    print(f"****** First Star = {star1}")

def star2(fileToOpen):
    instructions = readInstructionStar2(fileToOpen)
    print(instructions)
    
    max_row = instructions[0][0]
    max_col = instructions[0][1]
    robot = copy.deepcopy(instructions[1])
    boxes = copy.deepcopy(instructions[2])
    walls = copy.deepcopy(instructions[3])
    directions = copy.deepcopy(instructions[4])

    display2(max_row, max_col, robot, boxes, walls)
    while len(directions) > 0:
        direction = directions.pop(0)
        moveRobot2(robot, boxes, walls, direction)

    display2(max_row, max_col, robot, boxes, walls)    
    star2 = sum([box[0][0]*100+box[0][1] for box in boxes.values()])
    print(f"****** Second Star = {star2}")


fileToOpen = "./Day15.txt"
#star1(fileToOpen)
star2(fileToOpen)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 