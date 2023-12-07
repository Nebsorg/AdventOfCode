from datetime import datetime
from collections import defaultdict

#### Main
print("2023 --- Day 7: Camel Cards ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instructions = {}
    for i, line in enumerate(f):
        line = line.rstrip()
            
        hand = line.split()[0]
        bet = int(line.split()[1])

        instructions[hand] = bet
    return(instructions)


def typeStrength(hand):
    power = 0
    cardCount = defaultdict(lambda: 0)
    for c in hand:
        cardCount[c] += 1
    
    analyse = list(cardCount.values())
    if 5 in analyse:
        power += 7*10**8
        # print(f"hand={hand} ---> 5 of Kind -- Power = {power}")
    elif 4 in analyse:
        power += 6*10**8
        # print(f"hand={hand} ---> 4 of Kind -- Power = {power}")
    elif (3 in analyse) and (2 in analyse):
        power += 5*10**8
        # print(f"hand={hand} ---> FULL -- Power = {power}")
    elif 3 in analyse:
        power += 4*10**8
        # print(f"hand={hand} ---> 3 of Kind -- Power = {power}")
    elif 2 in analyse:
        ## how many pair ? 
        if analyse.count(2) == 2:
            power += 3*10**8
            # print(f"hand={hand} ---> 2 PAIR -- Power = {power}")
        else:
            power += 2*10**8
            # print(f"hand={hand} ---> 1 PAIR -- Power = {power}")
    return(power)



def localStrength(hand, rating):
    power = 0
    for i, c in enumerate(hand):
        power += rating[c]*20**(5-i)
    return(power)

def evaluateStrength(hand, rating):
    ## evalutation type
    power = typeStrength(hand)
    ## Evaluating hand : adding card local power    
    power += localStrength(hand, rating)
    return(power)


def evaluateStrenght_Joker(hand, rating):
    power = 0

    if hand == 'JJJJJ' or (not 'J' in hand):
        ## no jocker, or full jocker : keeping standard evaluation
        return(evaluateStrength(hand, rating))

    power = localStrength(hand, rating)

    ## We have at least one jocker : replacing it with the most present card the most present
    #  or in case of equality, with the higher one
    subhand = hand.replace('J', '')
    
    ## getting the cards the most represented :
    cardCount = defaultdict(lambda: 0)
    for i, c in enumerate(subhand):
        cardCount[c] += 1
    
    sorted_cardCount= sorted(cardCount,key=lambda x:cardCount[x], reverse=True)
    if len(sorted_cardCount) >= 2:
        if cardCount[sorted_cardCount[0]] == cardCount[sorted_cardCount[1]]:
            if rating[sorted_cardCount[0]] > rating[sorted_cardCount[1]]:
                cardReplace = sorted_cardCount[0]
            else:
                cardReplace = sorted_cardCount[1]
        else:
            cardReplace = sorted_cardCount[0]
    else:
        cardReplace = sorted_cardCount[0]

    ## replacing 
    newhand = hand.replace('J', cardReplace)
    power += typeStrength(newhand)
    return(power)    




def Firststar(instructions, rating):
    evaluatedHands = {}
    for hand, vet in instructions.items():
        power = evaluateStrength(hand,rating)
        evaluatedHands[hand] = power

    sorted_hands= sorted(evaluatedHands,key=lambda x:evaluatedHands[x])

    star = 0
    for i, hand in enumerate(sorted_hands):
        star += instructions[hand] * (i+1)
                    
    print(f"****** First Star = {star}")


def Secondstar(instructions, rating):
    rating['J'] = 1

    evaluatedHands = {}
    for hand, vet in instructions.items():
        power = evaluateStrenght_Joker(hand,rating)
        evaluatedHands[hand] = power

    sorted_hands= sorted(evaluatedHands,key=lambda x:evaluatedHands[x])

    star = 0
    for i, hand in enumerate(sorted_hands):
        star += instructions[hand] * (i+1)
                    
    print(f"****** Second Star = {star}")

rating = {}
for i in range(2,10):
    rating[str(i)] = i
rating['T'] = 10
rating['J'] = 11
rating['Q'] = 12
rating['K'] = 13
rating['A'] = 14


fileToOpen = "./2023/Day07.txt"
instructions = readInstruction(fileToOpen)
Firststar(instructions, rating)
Secondstar(instructions, rating)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 