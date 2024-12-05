from datetime import datetime
from collections import defaultdict

#### Main
print(f"2024 --- Day 5: Print Queue ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instructions = []
    rules = defaultdict(lambda: [])

    updates = []
    for line in f:
        line = line.rstrip()
        if line.count('|') == 1:
            rules[int(line.split('|')[0])].append(int(line.split('|')[1]))
        elif line.count(',') > 0:
            updates.append([int(x) for x in line.split(',')])

    instructions.append(rules)
    instructions.append(updates)
    return(instructions)

def checkValidity(update, rules):
    for i in range(len(update)):
        currentPage = update[i]
        followers = update[i+1:]
        for follower in followers:
            if currentPage in rules[follower]:
                return((i,update.index(follower)))
    return((-1,-1))        


def stars(instructions):
    star1 = 0
    star2 = 0

    rules = instructions[0]
    updates = instructions[1]

    for update in updates:
        validity = checkValidity(update,rules)
        if  validity == (-1,-1):
            ## update is valid
            #print(f"{update} is valide - midValue = {update[len(update)//2]}")
            star1 += update[len(update)//2]
        else:
            ## sorting invalide page
            #print(f"{update} is invalide on page {validity}")
            corrected_update = list(update)
            while validity != (-1,-1):
                corrected_update[validity[0]], corrected_update[validity[1]] = corrected_update[validity[1]], corrected_update[validity[0]]
                validity = checkValidity(corrected_update,rules)
            #print(f"{update} corrected to {corrected_update} - middle value={corrected_update[len(corrected_update)//2]}")
            star2 += corrected_update[len(corrected_update)//2]
            
    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day05.txt"
instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 