from datetime import datetime
import re
import math

#### Main
print("2023 --- Day 4: Scratchcards ---")
start_time = datetime.now()

regExp = "(\d+)"

fileToOpen = "./2023/Day04.txt"

f = open(fileToOpen, "r")

deck = {}
sum = 0
for i, line in enumerate(f):
    line = line.rstrip()
    
    winning = []
    possessed = []
    matches = re.finditer(regExp, line.split('|')[0])
    for i, match in enumerate(matches):
        if i == 0: 
            carte_ID = int(match.group())
        else:
            winning.append(int(match.group()))
    
    matches = re.finditer(regExp, line.split('|')[1])
    for i, match in enumerate(matches):
            possessed.append(int(match.group()))

    intersection = set(winning) & set(possessed)
    points = int(math.pow(2,len(intersection)-1))
    sum += points
    #print(f"Carte ID = {carte_ID} - Winning = {winning} - Possessed = {possessed} - intersection = {intersection} / {len(intersection)} - points = {points}")
    deck[carte_ID] = [1, len(intersection)]

##Star 02 : duplication of cards !
nbCard = 0
for id, datas in deck.items():
    qty = datas[0]
    nbCard += qty
    duplication = datas[1]
    #print(f"Card {id} - qty={qty} - duplication={duplication}")
    if duplication >= 1:
        for i in range(0,duplication):
            deck[id + i + 1][0] += qty
    
print(f"****** First Star = {sum}")
print(f"****** Second Star = {nbCard}")

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 