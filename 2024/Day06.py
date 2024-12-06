from datetime import datetime

#### Main
print(f"2024 --- Day 6: Guard Gallivant ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instructions = []
    area = []

    for i,line in enumerate(f):
        line = line.rstrip()
        max_col = len(line)
        for j, val in enumerate(line):
            match val:
                case '^':
                    guard = [[i,j], (-1,0)]
                case '<':
                    guard = [[i,j], (0,-1)]
                case '>':
                    guard = [[i,j], (0,1)]
                case 'v':
                    guard = [[i,j], (1,0)]
                case '#':
                    area.append((i,j))
    else:
        max_line = i+1 

    instructions.append(guard)
    instructions.append([area, max_line, max_col])
    return(instructions)

def getClosestObstacle(guard_pos, guard_dir, area, max_line, max_col):
    obstacles = []
    obstacle = None
    match guard_dir:
        case (-1,0):
            obstacles = [(i,j) for (i,j) in area if (i < guard_pos[0]) and (j - guard_pos[1]) == 0]
            if len(obstacles) == 0:
                obstacles.append((-1, guard_pos[1]))
        case (0,-1):
            obstacles = [(i,j) for (i,j) in area if (j < guard_pos[1]) and (i - guard_pos[0]) == 0]
            if len(obstacles) == 0:
                obstacles.append((guard_pos[0], -1))
        case (0,1):
            obstacles = [(i,j) for (i,j) in area if (j > guard_pos[1]) and (i - guard_pos[0]) == 0]
            if len(obstacles) == 0:
                obstacles.append((guard_pos[0], max_col))
        case (1,0):
            obstacles = [(i,j) for (i,j) in area if (i > guard_pos[0]) and (j - guard_pos[1]) == 0]
            if len(obstacles) == 0:
                obstacles.append((max_line, guard_pos[1]))

    
    if len(obstacles) > 1:
        for i,client in enumerate(obstacles):
            if i == 0:
                obstacle = client
            else:
                if ((guard_pos[0]-client[0])**2 + (guard_pos[1]-client[1])**2) < ((guard_pos[0]-obstacle[0])**2 + (guard_pos[1]-obstacle[1])**2):
                    obstacle = client
    else:
        obstacle = obstacles[0]
    return(obstacle)
    
def turnRight(direction):
    directions = [(-1,0), (0,1), (1,0), (0,-1)]

    i = directions.index(direction)
    i += 1
    if i >= len(directions):
        i = 0
    return(directions[i])

def explore(guard_pos, guard_dir, area, max_line, max_col):
    positionCrossed = set()
    positionCrossed.add((guard_pos[0], guard_pos[1]))

    guard_history = set()

    inMap = True
    while inMap:
        ## getting the closest obstacle in this direction:
        obstacle = getClosestObstacle(guard_pos, guard_dir, area, max_line, max_col)
        distance_i = (abs(obstacle[0]-guard_pos[0])-1)
        distance_j = (abs(obstacle[1]-guard_pos[1])-1)

        # print(f"{guard_pos=} - {guard_dir=} - NextObstacle = {obstacle}")

        ## adding all the crossed position to the history : 
        for i in range(max(distance_i, distance_j)+1):
            positionCrossed.add((guard_pos[0]+i*guard_dir[0], guard_pos[1]+i*guard_dir[1]))

        ## moving to the obstacle:
        guard_pos[0] += distance_i * guard_dir[0]
        guard_pos[1] += distance_j * guard_dir[1]

        ## turning right:
        guard_dir = turnRight(guard_dir)

        ## leaving the area
        if 0 < guard_pos[0] < max_line-1 and 0 < guard_pos[1] < max_col-1:
            inMap = True
        else: 
            inMap = False

        ## loop detection
        hist = (guard_pos[0], guard_pos[1], guard_dir[0], guard_dir[1])
        if hist in guard_history:
            return None
        else: 
            guard_history.add(hist)
       
    return(positionCrossed)

def explore_fast(guard_pos, guard_dir, area, max_line, max_col):
    guard_history = set()

    inMap = True
    while inMap:
        ## getting the closest obstacle in this direction:
        obstacle = getClosestObstacle(guard_pos, guard_dir, area, max_line, max_col)
        distance_i = (abs(obstacle[0]-guard_pos[0])-1)
        distance_j = (abs(obstacle[1]-guard_pos[1])-1)

        #print(f"{guard_pos=} - {guard_dir=} - NextObstacle = {obstacle}")

        ## moving to the obstacle:
        guard_pos[0] += distance_i * guard_dir[0]
        guard_pos[1] += distance_j * guard_dir[1]

        ## turning right:
        guard_dir = turnRight(guard_dir)

        ## leaving the area
        if 0 < guard_pos[0] < max_line-1 and 0 < guard_pos[1] < max_col-1:
            inMap = True
        else: 
            inMap = False

        ## loop detection
        hist = (guard_pos[0], guard_pos[1], guard_dir[0], guard_dir[1])
        if hist in guard_history:
            return True
        else: 
            guard_history.add(hist)
       
    return(False)

def stars(instructions):
    star1 = 0
    star2 = 0

    guard_pos = list(instructions[0][0])
    guard_dir = instructions[0][1]
    area = instructions[1][0]
    max_line = instructions[1][1]
    max_col = instructions[1][2]
    
    positionCrossed = explore(guard_pos, guard_dir, area, max_line, max_col)
    star1 = len(positionCrossed)

    for i in range(max_line):
        for j in range(max_col):
            guard_pos = list(instructions[0][0])
            guard_dir = instructions[0][1]

            if (i,j) in area:
                continue

            if (i,j) == (guard_pos[0], guard_pos[1]):
                continue
            
            area.append((i,j))
            positionCrossed = explore_fast(guard_pos, guard_dir, area, max_line, max_col)
            if positionCrossed:
                star2 += 1
            area.pop()

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day06.txt"
instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 