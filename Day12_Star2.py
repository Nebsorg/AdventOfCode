from datetime import datetime
import copy
import math

def moveWaypoint(waypoint, value, instruction):
    if instruction == 'N':
        waypoint[1] += value
    elif instruction == 'S':
        waypoint[1] -= value
    elif instruction == 'E':
        waypoint[0] += value
    elif instruction == 'W':
        waypoint[0] -= value
    if instruction == 'R':
        shift = int(value / 90)
        for i in range(shift):
            temp = waypoint[0]
            waypoint[0] = waypoint[1]
            waypoint[1] = -temp
    elif instruction == 'L':
        shift = int(value / 90)
        for i in range(shift):
            temp = waypoint[0]
            waypoint[0] = -waypoint[1]
            waypoint[1] = temp
    return(waypoint)


if __name__ == '__main__':
    start_time = datetime.now()

    orientatinVector = ['N', 'E', 'S', 'W']
    boatPosition = [0,0] ## East / North
    waypoint = [10, 1] ## North / East

    f = open("Z:\donnees\developpement\Python\AdventOfCode\day12.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        instruction = line[0]
        value = int(line[1:])

        if instruction == 'F':
            boatPosition[0] += value * waypoint[0]
            boatPosition[1] += value * waypoint[1]
        else:
            waypoint = moveWaypoint(waypoint, value, instruction)
    f.close()
    print(f"Star2 = {abs(boatPosition[0]) + abs(boatPosition[1])}")

    ##Duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
