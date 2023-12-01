from datetime import datetime
from num2words import num2words

#### Main
print("2023 --- Day 1: Trebuchet?! ---")
start_time = datetime.now()

fileToOpen = ".\Day01.txt"


def firstStar():
    f = open(fileToOpen, "r")
    sum = 0
    for line in f:
        line = line.rstrip()
        digits = [d for d in line if d.isdigit()]
        value = int(digits[0]+digits[-1])
        sum+=value
    print(f"****** First Star = {sum}")


def secondStar():
    f = open(fileToOpen, "r")
    sum = 0
    ## constructing array of digit to find in the text
    wordToCheck = {}
    for i in range(0, 10):
        wordToCheck[str(i)] = str(i)
        if i != 0 :
            wordToCheck[num2words(i)] = str(i)

    for line in f:
        line = line.rstrip()
        digits = []

        for i in range(0,len(line)):
            for word in wordToCheck.keys():
                if word == line[i:len(word)+i]:
                    digits.append(wordToCheck[word])
                    break
           
        value = int(digits[0]+digits[-1])
        sum+=value
    
    print(f"****** Second Star = {sum}")

firstStar()
secondStar()


end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 