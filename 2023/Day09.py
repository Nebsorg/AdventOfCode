from datetime import datetime
import math

#### Main
print("2023 --- Day 9: Mirage Maintenance ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instructions = {}
    for i, line in enumerate(f):
        line = line.rstrip()

        instructions[i] = list(map(int,line.split()))
    return(instructions)

def evaluate(vector):
    levels = {}
    depth = 0
    finished = False
    levels[depth] = list(vector)
    ## top -> down to reach '0' line
    while not finished:
        current_vector = levels[depth]
        for val in current_vector:
            if val != 0:
                break
        else:
            ## all 0
            finished = True

        if not finished:
            depth += 1
            next_vector = []
            for i in range(len(current_vector)-1):
                next_vector.append(current_vector[i+1]-current_vector[i])
            levels[depth] = next_vector
    #print(f"Vector {vector} -- Bottom reached in {depth} steps --> {levels}")

    ## bottom -> up
    for depth in range(len(levels.keys())-2, -1, -1):
        ## print(f"B-U - depth={depth} - {levels[depth]} - newVal = {new_val}")
        levels[depth].append(levels[depth][-1]+levels[depth+1][-1])
        levels[depth].insert(0, levels[depth][0]-levels[depth+1][0])

    return(levels[0][0], levels[0][-1])

def stars(instructions):
    star1 = 0
    star2 = 0
    for vector in instructions.values():
        r1, r2 = evaluate(vector)
        star1 += r2
        star2 += r1
    
    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")



fileToOpen = "./2023/Day09.txt"
instructions = readInstruction(fileToOpen)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 