from datetime import datetime
from llist import dllist, dllistnode
import copy


def printcup(cups, currentCup):
    result = ""
    for cup in cups:
        if cup == currentCup:
            result += f" ({cup})"
        else:
            result += f" {cup}"
    return(result)

def score(cups):
    result = ""
    node = moveNext(findNode(1, cups), cups)
    for i in range(len(cups)-1):
        result += str(node.value)
        node = moveNext(node, cups)
    return(result)

def pickup(cups, currentCup):
    pickedup = []
    pos = cups.index(currentCup)+1
    for i in range(3):
        if pos < len(cups):
            pickedup.append(cups.pop(pos))
        else:
            pickedup.append(cups.pop(0))
    return(pickedup)

def getDestinationValue(max, currentCup, pickedup):
    found = False
    searchValue = currentCup - 1
    min = 1
    while not found:
        if searchValue < min:
            while not found:
                if max in pickedup:
                    max -= 1
                else:
                    return(max)

        if searchValue in pickedup:
            searchValue -= 1
        else:
            return(searchValue)

def insertCups(cups, destinationPos, toInsert):
    return(cups[:destinationPos+1]+toInsert+cups[destinationPos+1:])

def findNode(value, cups):
    ## fast implementation : checking if initiale position has been moveId
    node = cups.first
    while node.value != value:
        node = node.next
    return(node)

def moveNext(currentCup, cups):
    next = currentCup.next
    if next == None:
        next = cups.first
    return(next)

def star1(cups_input):
    cups = dllist(cups_input)
    max = len(cups)
    currentCup = cups.first

    for moveId in range(100):
        #print(f"-- move {moveId+1} --")
        #print(f"cups: {printcup(cups, currentCup.value)}")

        ## move to next node to remove them from the list
        pickedup = []
        nextCup = currentCup
        for i in range(3):
            nextCup = moveNext(nextCup, cups)
            pickedup.append(nextCup.value)

        #print(f"pick up: {pickedup}")
        destinationValue = getDestinationValue(max, currentCup.value, pickedup)
        destinationCup = findNode(destinationValue, cups)
        #print(f"Destination Value={destinationValue}")

        ## remove Cup:
        for i in range(3):
            nextCup = moveNext(currentCup, cups)
            cups.remove(nextCup)

        ## insert cups:
        nextCup = moveNext(destinationCup, cups)
        for i, nb in enumerate(pickedup):
            cups.insert(nb, nextCup)
        currentCup = moveNext(currentCup, cups)

    #print(f"final: {printcup(cups, currentCup)}")
    print(f"star1: {score(cups)}")

def star2(cups_input):
    cups = dllist(cups_input)
    maxValue = 1000000
    currentCup = cups.first

    beginTime = datetime.now()
    moveTotal = 100000
    for moveId in range(100000):
        #print(f"-- move {moveId+1} --")
        #print(f"cups: {printcup(cups, currentCup.value)}")
        if moveId%10000 == 0 and moveId > 0:
            currentTime = datetime.now()
            elapsedTime = currentTime - beginTime
            print(f"#{moveId} : elapsedTime={elapsedTime} - estimatedRemaningTime={elapsedTime*moveTotal/moveId}")

        ## move to next node to remove them from the list
        pickedup = []
        nextCup = currentCup
        for i in range(3):
            nextCup = moveNext(nextCup, cups)
            pickedup.append(nextCup.value)
        #print(f"pick up: {pickedup}")
        destinationValue = getDestinationValue(maxValue, currentCup.value, pickedup)
        ## testing if destinationValue is in the actual list or not


        destinationCup = findNode(destinationValue, cups)
        #print(f"Destination Value={destinationValue}")

        ## remove Cup:
        for i in range(3):
            nextCup = moveNext(currentCup, cups)
            cups.remove(nextCup)

        ## insert cups:
        nextCup = moveNext(destinationCup, cups)
        for i, nb in enumerate(pickedup):
            cups.insert(nb, nextCup)

        currentCup = moveNext(currentCup, cups)

    #print(f"final: {printcup(cups, currentCup)}")
    print('fini')

    ## searching one :
    oneNode = findNode(1, cups)
    star1Node = moveNext(oneNode, cups)
    star2Node = moveNext(star1Node, cups)

    print(f"Star1={star1Node.value} - Star2={star2Node.value} - mult={star1Node.value*star2Node.value}")



if __name__ == '__main__':
    start_time = datetime.now()
    cups_test = [3,8,9,1,2,5,4,6,7]
    cups_real = [7,1,2,6,4,3,5,8,9]

    cups = cups_test.copy()
    star1(cups)
    cups = cups_test.copy()
    star2(cups)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
