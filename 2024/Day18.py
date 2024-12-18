from datetime import datetime
from collections import deque

#### Main
print(f"2024 --- Day 18: RAM Run ---")
start_time = datetime.now()

def display(max_x, max_y, nanosecond, corruptedZones, path):
    for y in range(max_y):
        line = ""
        for x in range(max_x):
            if (x,y) in path: line+='O'
            elif (x,y) in corruptedZones[nanosecond]: line+='#'
            else: line+='.'
        print(line)
    return(0)

def readInstruction(file):
    f = open(file, "r")
    corruptedZones = {}
    for i,line in enumerate(f):
        line = line.rstrip()
        if i == 0:
            corruptedZones[i] = []
        else:
            corruptedZones[i] = list(corruptedZones[i-1])
        corruptedZones[i].append((int(line.split(',')[0]), int(line.split(',')[1])))
    maxByte = max(corruptedZones.keys())

    return([maxByte, corruptedZones])

def dijkstraFast(size, start_pos, time, corruptedZone):
    node_bag = deque([start_pos])
    costMap = {start_pos: 0}
    max_x = size[0]
    max_y = size[1]

    while node_bag:
        ## taking a node
        
        test_node = node_bag.popleft()
        ## checking Neighbours
        for shift in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_pos = (test_node[0] + shift[0], test_node[1] + shift[1])
            if new_pos[0] < 0 or new_pos[0] >= max_x or new_pos[1] < 0 or new_pos[1] >= max_y:
                continue
            
            if (new_pos[0], new_pos[1]) in corruptedZone[time]:
                continue

            ## updating neighbour cost
            risk = costMap[test_node] + 1

            if new_pos in costMap:
                if risk < costMap[new_pos]:
                    ## meilleur chemin, on remplace l'existant
                    costMap[new_pos] = risk
                    node_bag.append(new_pos)
            else:
                    ## premier pasage, on memorise
                    costMap[new_pos] = risk
                    node_bag.append(new_pos) 
    return costMap

def stars(instructions):
    star1 = 0
    star2 = 0

    max_x = 71
    max_y = 71
    target = (70,70)
    time = 1023

    ## données de test : 
    #max_x = 7
    #max_y = 7
    #target = (6,6)
    #time = 11

    maxByte = instructions[0]
    corruptedZones = instructions[1]
    
    #display(max_x, max_y, time, corruptedZones, [])
    costMap = dijkstraFast((max_x, max_y), (0,0), time, corruptedZones)
    star1 = costMap[target]
    print(f"****** First Star = {star1}")

    ## on regarde quand la target devient accessible plutot que quand elle ne l'est plus : bien plus rapide !
    for i in range(maxByte,0,-1):
        costMap = dijkstraFast((max_x, max_y), (0,0), i, corruptedZones)
        if not target in costMap.keys():
            #print(f"{i+1} bytes has fall : target not accessible")
            continue
        else:
            #print(f"{i+1} bytes has fall : target is now accessible in {costMap[target]} moves")
            blockingTime = i+1
            star2 = corruptedZones[i+1][-1]
            break


    #display(max_x, max_y, blockingTime, corruptedZones, [])
    print(f"****** Second Star = {star2}")  

fileToOpen = "./Day18.txt"

instructions = readInstruction(fileToOpen)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 