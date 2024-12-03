from datetime import datetime
from num2words import num2words
import numpy as np

#### Main
print("2024 --- Day 1: Historian Hysteria ---")
start_time = datetime.now()

fileToOpen = "./Day01.txt"

def getData(fileToOpen):
    f = open(fileToOpen, "r")
    listA = []
    listB = []
    for line in f:
        a,b = line.split("   ")
        listA.append(int(a))
        listB.append(int(b))
    listA.sort()
    listB.sort()
    return(listA, listB)

def firstStar(listA, listB):
    distance = 0
    for i in range(len(listA)):
        distance += abs(listA[i]-listB[i])

    print(f"****** First Star = {distance}")


def secondStar(listA, listB):
    similarity = 0
    
    for i in range(len(listA)):
        similarity += listA[i]*np.count_nonzero(listB == listA[i])

    print(f"****** Second Star = {similarity}")



listA, listB = getData(fileToOpen)
firstStar(listA, listB)
secondStar(np.array(listA), np.array(listB))


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 