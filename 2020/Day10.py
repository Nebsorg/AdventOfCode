from collections import defaultdict
from datetime import datetime

def computeNode(numberList, position, history):
    pathNumber = 0
    history.append(numberList[position])
    if (position == len(numberList) - 1):
        ## on a atteind+ la fin de la liste, on a trouvé un chemin valide
        print(f"Chemin trouvee numberList[{position}]={numberList[position]} - nodeNumber={pathNumber} - history={history}")
        return(1)

    ## sinon, on explore les possibilité à partir de cette position
    for i in range(1,4):
        if position + i < len(numberList):
            ## est-ce qu'on peut utiliser cet adapteur
            if 1 <= numberList[position + i] - numberList[position] <= 3:
                subHistory = history.copy()
                pathNumber += computeNode(numberList, position + i, subHistory)
    return(pathNumber)

def computeNodeFast(numberList, position):
    if position in alreadycomputed:
        return(alreadycomputed[position])

    pathNumber = 0
    if (position == len(numberList) - 1):
        ## on a atteind+ la fin de la liste, on a trouvé un chemin valide
        return(1)

    ## sinon, on explore les possibilité à partir de cette position
    for i in range(1,4):
        if position + i < len(numberList):
            ## est-ce qu'on peut utiliser cet adapteur
            if 1 <= numberList[position + i] - numberList[position] <= 3:
                pathNumber += computeNodeFast(numberList, position + i)
    alreadycomputed[position]=pathNumber
    return(pathNumber)



start_time = datetime.now()

numberList = [0]
f = open("Z:\donnees\developpement\Python\AdventOfCode\day10.txt", "r")
for line in f:
    numberList.append(int(line.rstrip("\n")))
f.close()

## Star 1
numberList.sort()
numberList.append(numberList[-1]+3)
delta = defaultdict(lambda: 0)
previousAdaptor = numberList[0]
for i in range(1,len(numberList)):
    delta[numberList[i]-previousAdaptor] += 1
    previousAdaptor = numberList[i]
print(f"star1 : {delta[1]*delta[3]}")

## Star 2
#history = []
#print(f"star2 : {computeNode(numberList,0, history)}")

alreadycomputed={}
print(f"star2 : {computeNodeFast(numberList,0)}")

end_time = datetime.now()
print('Duration: {}'.format(end_time - start_time))
