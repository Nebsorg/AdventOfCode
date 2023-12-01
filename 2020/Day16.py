from datetime import datetime
import re

def parseEntry():
    regexp = "(?P<RuleName>.*): (?P<val1Min>\d+)-(?P<val1Max>\d+) or (?P<val2Min>\d+)-(?P<val2Max>\d+)"
    rules = {}
    nearbyTickets = []
    ruleID = 1
    currentSection = "rules"
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day16.txt", "r")
    for line in f:
        line = line.rstrip("\n")
        if line == "your ticket:":
            currentSection = "my"
        elif line == "nearby tickets:":
            currentSection = "nearby"
        elif line == "":
            continue
        else:
            if currentSection == "rules":
                match = re.match(regexp, line)
                if match:
                    ruleName = match.group('RuleName')
                    val1Min = int(match.group('val1Min'))
                    val1Max = int(match.group('val1Max'))
                    val2Min = int(match.group('val2Min'))
                    val2Max = int(match.group('val2Max'))
                    rules[ruleName] = [val1Min, val1Max, val2Min, val2Max, []]
            elif currentSection == "my":
                myTickets = list(map(int, line.split(',')))
            else:
                nearbyTickets.append(list(map(int, line.split(','))))
    f.close()
    return rules, myTickets, nearbyTickets

def matchRules(number, rules):
    for rule in rules.values():
        if matchRule(number, rule):
            return(True)
    return(False)

def matchRule(number, rule):
    return((rule[0] <= number <= rule[1]) or (rule[2] <= number <= rule[3]))

def removeIndexfromOtherRule(index, ruleToKeep, rules):
    for name, rule in rules.items():
        if name != ruleToKeep:
            if index in rule[4]:
                rule[4].remove(index)

def star2(nearbyValidTicket, rules, myTickets):
    ## creating all possible index for each rules :
    for name, rule in rules.items():
        unpossibleIndex = set()
        for ticket in nearbyValidTicket:
            for index in range(len(ticket)):
                if not matchRule(ticket[index], rule):
                    unpossibleIndex.add(index)

        AllIndex = set(range(len(myTickets)))
        ruleIndexes = list(AllIndex - unpossibleIndex)
        rule[4] = ruleIndexes

    ## now each rules contain a list of possible position, trying to affect only one
    departurekeys = [key for key in rules if key.startswith("departure")]

    departureIdentified = False
    while not departureIdentified:
        for name, rule in rules.items():
            if len(rule[4]) == 1:
                ## unique index found for this rule, removing it from other rules
                removeIndexfromOtherRule(rule[4][0], name, rules)

        departureIdentified = True
        for key in departurekeys:
            departureIdentified = departureIdentified and (len(rules[key][4]) == 1)

    ## checking on my tickets
    total = 1
    for key in departurekeys:
        index = rules[key][4][0]
        total *= myTickets[index]

    print(f"Star2 = {total}")

def star1():
    rules, myTickets, nearbyTickets = parseEntry()
    TSE = 0
    nearbyValidTicket = nearbyTickets.copy()
    for ticket in nearbyTickets:
        for number in ticket:
            if not matchRules(number, rules):
                TSE += number
                nearbyValidTicket.remove(ticket)
    print(f"Star1 = {TSE}")
    return(nearbyValidTicket, rules, myTickets)

if __name__ == '__main__':
    start_time = datetime.now()
    nearbyValidTicket, rules, myTickets = star1()
    star2(nearbyValidTicket, rules, myTickets)
    ##Duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
