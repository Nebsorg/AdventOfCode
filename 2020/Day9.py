
def testNumber(liste, testNumber):
    for i in range(len(liste)):
        for j in range(i+1, len(liste)):
            if liste[i]+liste[j] == currentNumber:
                return True, liste[i], liste[j]
    return False, -1, -1

def testSequenceFromIndex(liste, invalideNumber, index):
    currentSum = 0
    for i in range(index, len(liste)):
        currentSum += liste[i]
        if currentSum == invalidNumber:
            return True, i+1
        elif currentSum > invalidNumber:
            return False, -1
    return False, -1

numberList = []
preamble = 25
f = open("Z:\donnees\developpement\Python\AdventOfCode\day9.txt", "r")
numberRead = 1
for line in f:
    currentNumber = int(line.rstrip("\n"))

    ## preamble numbers : initializing the list of available numbers
    if numberRead <= preamble:
        numberList.append(currentNumber)
        #print("#{0}={1} - preamble not completed, adding it to availableNumbers".format(numberRead, currentNumber))
    else:
        ## validating number : is it the sum of two numbers in the premable last number of the list
        testResult, a, b = testNumber(numberList[-preamble:], currentNumber)
        if testResult:
            numberList.append(currentNumber)
            #print("#{0}={1} - number valide - is the sum of {2} and {3}".format(numberRead, currentNumber, a, b))
        else:
            invalidNumber = currentNumber
            print("Star 1 : {1} - #{0}={1} - number NOT valide".format(numberRead, invalidNumber, a, b))
            break
    numberRead += 1
f.close()

## Star 2 : looking for a set of addition with all previous numbers :
for i in range(len(numberList)):
    testResult, shift = testSequenceFromIndex(numberList, invalidNumber, i)
    if testResult:
        listResult = numberList[i:shift]
        print("Star 2 : {1} - sublist={0}".format(listResult, min(listResult) + max(listResult)))
        break
