import os

import copy

from datetime import datetime
from collections import deque
import pygame


g_windowsWidth = 1000
g_windowsHeight = 1000
g_grey_color = (127,127,127)
g_openNode = (55,55,55)
g_closeNode = (175, 175, 175)
g_currentNode = (255,0,0)
g_otherNode = (255,255,255)
g_boardScreenSize = 1000

g_heatColor = [(255,247,236), (254,232,200), (253,212,158), (253,187,132), (252,141,89), (239,101,72), (215,48,31),(179,0,0),(127,0,0)]

def render(path):

    ## draw background
    color = g_grey_color
    pygame.draw.rect(g_screen, color, (0, 0, g_windowsWidth, g_windowsHeight))

    x_shift = int(g_boardScreenSize / g_width)
    y_shift = int(g_boardScreenSize / g_height)


    # for i in range(g_width + 1):
    #     pygame.draw.line(g_screen, color, (i * x_shift, 0), (i * x_shift, g_boardScreenSize))
    # for i in range(g_height + 1):
    #     pygame.draw.line(g_screen, color, (0, i * y_shift), (g_boardScreenSize, i * y_shift))

    color = (0,0,0)
    pygame.draw.rect(g_screen, color, (0, 0, g_boardScreenSize, g_boardScreenSize))

    color = (0, 255, 0)
    pygame.draw.rect(g_screen, color, (0,0, x_shift, y_shift))
    pygame.draw.rect(g_screen, color, (g_boardScreenSize, g_boardScreenSize, x_shift, y_shift))

    for y in range(g_height):
        for x in range(g_width):
            pygame.draw.rect(g_screen, g_heatColor[g_maze[y][x]-1], (x*x_shift, y*y_shift, x_shift, y_shift))

    for node in path:
        color = (255,0,255)
        pygame.draw.rect(g_screen, color, (node[0] * x_shift, node[1] * y_shift, x_shift, y_shift))

    pygame.display.flip()
    pygame.event.pump()


def extendMaze(maze):
    ## extend existing column:
    for y in range(len(maze)):
        line = maze[y]
        lineSize = len(line)
        for i in range(1, 5):
            for x in range(lineSize):
                newVal = line[x] + i
                if newVal > 9:
                    newVal = newVal % 10 + 1
                line.append(newVal)
    # print_maze(maze,x_sep, y_sep)

    initialHeight = len(maze)
    ## extending line:
    for i in range(initialHeight * 4):
        line = maze[i]
        lineToAdd = []
        for x in range(len(line)):
            newVal = line[x] + 1
            if newVal > 9:
                newVal = newVal % 10 + 1
            lineToAdd.append(newVal)
        maze.append(lineToAdd)

def dijkstraFast(maze, start_node, refreshRate):

    node_bag = deque([start_node])
    costMap = {start_node: 0}
    size_x = len(maze[0])
    size_y = len(maze)
    step = 1
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

        if step%(refreshRate) == 0:
            path = getPathReverse(maze, costMap, start_node, current_node)
            render(path)
        step += 1
    return costMap

def getPathReverse(maze, costmap, start, end):
    current_node = end
    path = [end]
    size_x = len(maze[0])
    size_y = len(maze)
    step = 0
    while current_node != start:
        nearNode = {}
        for shift in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_node = (current_node[0] + shift[0], current_node[1] + shift[1])
            if new_node[0] >= size_x or new_node[0] < 0 or new_node[1] >= size_y or new_node[1] < 0:
                continue

            if new_node in path:
                continue

            if (new_node[0],new_node[1]) in costmap:
                nearNode[new_node] = costmap[(new_node[0],new_node[1])]
            else:
                nearNode[new_node] = size_x*size_y*9

        ##print(f"** step {step} : current node = {current_node} - NearNode={nearNode}")
        lowest = min(nearNode, key=nearNode.get)
        current_node = lowest
        path.append(current_node)
        step += 1
    return(path)



def main():
    global g_screen
    global g_maze
    global g_height
    global g_width

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("--- Day 15: Chiton ---")

    # create a surface on screen
    g_screen = pygame.display.set_mode((g_windowsWidth, g_windowsHeight))
    pygame.font.init()
    global myfont
    myfont = pygame.font.SysFont('Comic Sans MS', 20)

    g_maze = []
    f = open(".\Day15.txt", "r")
    i = 0
    for line in f:
        l = [int(v) for v in line.rstrip()]
        g_maze.append(l)
    f.close()

    initialMaze = copy.deepcopy((g_maze))
    extendMaze(g_maze)
    largeMaze = copy.deepcopy((g_maze))

    g_height = len(g_maze)
    g_width = len(g_maze[0])


    render([])
    running = True
    # main loop
    path = []
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    path = []
                    g_maze = copy.deepcopy(initialMaze)
                    g_height = len(g_maze)
                    g_width = len(g_maze[0])

                if event.key == pygame.K_RIGHT:
                    path=[]
                    g_maze = copy.deepcopy(largeMaze)
                    g_height = len(g_maze)
                    g_width = len(g_maze[0])

                if event.key == pygame.K_UP:
                    g_maze = copy.deepcopy(initialMaze)
                    g_height = len(g_maze)
                    g_width = len(g_maze[0])

                    print(f"Start Resolution")
                    cost_map = dijkstraFast(g_maze, (0, 0), 100)
                    print(f"Resolved")
                    path = getPathReverse(g_maze, cost_map, (0,0), (g_width-1, g_height-1))
                    #print(f"Path computed : {path}")

                    pygame.event.clear()
                if event.key == pygame.K_DOWN:
                    g_maze = copy.deepcopy(largeMaze)
                    g_height = len(g_maze)
                    g_width = len(g_maze[0])
                    print(f"Start Resolution")
                    cost_map = dijkstraFast(g_maze, (0, 0), 45000)
                    print(f"Resolved")
                    path = getPathReverse(g_maze, cost_map, (0, 0), (g_width - 1, g_height - 1))
                    pygame.event.clear()
        render(path)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    print("--- Day 15: Chiton ---")
    #### Main
    start_time = datetime.now()

    # call the main function
    directoryPath = os.path.dirname(__file__)
    print(directoryPath)

    main()

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))

