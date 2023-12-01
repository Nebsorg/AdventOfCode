from datetime import datetime
from collections import deque

print("--- Day 15: Chiton ---")
#### Main
start_time = datetime.now()

def print_maze(maze, x_sep, y_sep):
    width = len(maze[0])

    for y,line in enumerate(maze):
        prtLine = ''
        if y%y_sep == 0:
            print('-'*width)
        for x,val in enumerate(line):
            if x%x_sep == 0:
                prtLine += '|'
            prtLine += str(val)
        print(prtLine)

def dijkstraFast(maze, start_node):

    node_bag = deque([start_node])
    costMap = {start_node: 0}
    size_x = len(maze[0])
    size_y = len(maze)

    while node_bag:
        ## taking a node
        current_node = node_bag.popleft()

        ## checking Neighbours
        for shift in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_node = (current_node[0] + shift[0], current_node[1] + shift[1])
            if new_node[0] >= size_x or new_node[0] < 0 or new_node[1] >= size_y or new_node[1] < 0:
                continue

            ## updating neighbour cost
            risk = costMap[current_node] + maze[new_node[0]][new_node[1]]
            if new_node not in costMap or risk < costMap[new_node]:
                costMap[new_node] = risk
                node_bag.append(new_node)
    return costMap

maze = []
f = open(".\Day15.txt", "r")
i = 0
for line in f:
    l = [int(v) for v in line.rstrip()]
    maze.append(l)
f.close()

x_max = len(maze[0])
y_max = len(maze)

mid_time = datetime.now()
cost_map = dijkstraFast(maze, (0, 0))
end_time = datetime.now()
print(f"** First Star = {cost_map[(x_max - 1, y_max - 1)]} - {(end_time - mid_time)}")

## creating the new maze:

## extend existing column:
for y in range(len(maze)):
    line = maze[y]
    lineSize = len(line)
    for i in range(1,5):
        for x in range(lineSize):
            newVal = line[x]+i
            if newVal > 9:
                newVal = newVal%10 + 1
            line.append(newVal)
#print_maze(maze,x_sep, y_sep)

initialHeight = len(maze)
## extending line:
for i in range(initialHeight*4):
    line = maze[i]
    lineToAdd = []
    for x in range(len(line)):
        newVal = line[x] + 1
        if newVal > 9:
            newVal = newVal % 10 + 1
        lineToAdd.append(newVal)
    maze.append(lineToAdd)

x_max = len(maze[0])
y_max = len(maze)

mid_time = datetime.now()
cost_map = dijkstraFast(maze, (0, 0))
end_time = datetime.now()
print(f"** Second Star = {cost_map[(x_max - 1, y_max - 1)]} - {(end_time - mid_time)}")


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))