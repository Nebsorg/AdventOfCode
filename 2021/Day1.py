print("Day 1 !")

def firstStar(listOfDepth):
    increaseTime = 0
    for i in range(1,len(listOfDepth)):
        if listOfDepth[i] > listOfDepth[i-1]:
            increaseTime += 1
    print("  ** First Star : %d" % increaseTime)

def secondStar(listOfDepth):
    increaseTime = 0
    for i in range(3,len(listOfDepth)):
        if sum(listOfDepth[i-2:i+1]) > sum(listOfDepth[i-3:i]):
            increaseTime += 1
    print("  ** Second Star : %d" % increaseTime)

f = open(".\Day1.txt", "r")
listOfDepth = []
for line in f:
    listOfDepth.append(int(line))
f.close()

firstStar(listOfDepth)
secondStar(listOfDepth)

