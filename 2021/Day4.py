from datetime import datetime
import copy

print("Day 4 !")

def secondStar(boards, drawnNumbersList):
    while len(boards) > 0:
        currentNumber = drawnNumbersList.pop(0)
        #print(f"Playing {currentNumber} -- Number of Boards still in game : {len(boards)}")

        for board in boards:
            for vector in board:
                for value in vector:
                    if value[0] == currentNumber:
                        value[1] = 1

        newBoards = []
        for id, board in enumerate(boards):
            if winBoard(board) == False:
                newBoards.append(board)
                #print(f"  - Board {id} is not winning - keeping it")
            #else:
                #print(f"  - Board {id} won ! removing it")

        boards = newBoards

    sumUnmarked = 0
    for i in range(5):
        for j in range(5):
            if board[i][j][1] == 0:
                sumUnmarked += int(board[i][j][0])
    print(f"  ** Second Star : Last board victory with number = {currentNumber} / Somme of unmarked number = {sumUnmarked} / second star={sumUnmarked * int(currentNumber)}")

def winBoard(board):
    for vector in board:
        if winVector(vector):
            return(True)
    return(False)

def winVector(vector):
    for value in vector:
        if value[1] == 0:
            return(False)
    return(True)


def play(currentNumber, boards):
    ## mark number
    for board in boards:
        for vector in board:
            for value in vector:
                if value[0] == currentNumber:
                    value[1] = 1
            ## check victory:
            if winVector(vector):
                #print(f"Victory with number {currentNumber}")
                return (True, board)
    return(False, [])

def firstStar(boards, drawnNumbersList):
    win = False
    while not(win):
        ## draw number:
        currentNumber = drawnNumbersList.pop(0)
        win, board = play(currentNumber, boards)

    sumUnmarked = 0
    for i in range(5):
        for j in range(5):
            if board[i][j][1] == 0:
                sumUnmarked += int(board[i][j][0])

    print(f"  ** First Star : Victory with number = {currentNumber} / Somme of unmarked number = {sumUnmarked} / first star={sumUnmarked * int(currentNumber)}")




start_time = datetime.now()

f = open(".\Day4.txt", "r")
instructions = []
lineId = 0
boards = []
currentBoard = []
for line in f:
    if lineId == 0:
        drawnNumbersList = line.rstrip().split(',')
    else:
        if line == '\n':
            # finishing or starting a board
            if currentBoard != []:
                boards.append(currentBoard)
                currentBoard = []
        else:
            currentBoard.append([[v,0] for v in line.rstrip().split()])
    lineId += 1
f.close()
boards.append(currentBoard)

print(f"Numbers of boards: {len(boards)} - Number of numbers = {len(drawnNumbersList)}")

## adding columns as vector
for board in boards:
    columns = []
    for i in range(5):
        for j in range(5):
            if i == 0:
                columns.append([])
            columns[j].append((board[i][j]))
    board += columns

boardsStar2 = copy.deepcopy(boards)
drawnNumbersListStar2 = copy.deepcopy(drawnNumbersList)
firstStar(boards, drawnNumbersList)
secondStar(boardsStar2, drawnNumbersListStar2)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time))