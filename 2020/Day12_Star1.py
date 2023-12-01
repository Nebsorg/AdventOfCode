from datetime import datetime
import copy

def moveCardinal(position, value, instruction):
    if instruction == 'N':
        position[0] += value
    elif instruction == 'S':
        position[0] -= value
    elif instruction == 'E':
        position[1] += value
    elif instruction == 'W':
        position[1] -= value
    return(position)


if __name__ == '__main__':
    start_time = datetime.now()

    orientatinVector = ['N', 'E', 'S', 'W']
    orientation = 1
    position = [0,0] ## North / East

    f = open("Z:\donnees\developpement\Python\AdventOfCode\day12.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        instruction = line[0]
        value = int(line[1:])
        if instruction == 'R':
            shift = value / 90
            orientation = int((orientation + shift)%4)
        elif instruction == 'L':
            shift = value / 90
            orientation = int((orientation - shift)%4)
        elif instruction == 'F':
            position = moveCardinal(position, value, orientatinVector[orientation])
        else:
            position = moveCardinal(position, value, instruction)
    f.close()
    print(f"Star1 = {abs(position[0]) + abs(position[1])}")

    ##Duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
