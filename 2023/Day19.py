from datetime import datetime
import re
from tools import Style
from tools import split_interval
from collections import defaultdict
import copy

#### Main
print(f"{Style.RED}2023 --- Day 19: Aplenty ---{Style.RESET}")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    workflows = defaultdict(lambda: [])
    ratings = []

    ## read all instruction : 
    section = 'workflows'
    for i,line in enumerate(f):
        line = line.rstrip()

        if line == '':
            section = 'ratings'
        else:
            if section == 'workflows':
                pos = line.find('{')
                wf_name = line[0:pos]
                wf_rules = line[pos+1:len(line)-1].split(',')
                parsed_rules = []
                for rule in wf_rules:
                    pos = rule.find(':')
                    if pos >= 0:
                        caracteristic = rule[0]
                        operande = rule[1]
                        pos = rule.find(':')
                        value = int(rule[2:pos])
                        destination = rule[pos+1:]
                        parsed_rules = [operande, destination, caracteristic, value]
                    else:
                        operande = '*'
                        destination = rule
                        parsed_rules = [operande, destination]
                    workflows[wf_name].append(parsed_rules)
            else:
                values = line[1:len(line)-1].split(',')
                attribut = {}
                for value in values:
                    a_name = value[0]
                    a_val = int(value[2:])
                    attribut[a_name] = a_val
                ratings.append(attribut)

    return(workflows, ratings)


def applyRules(rules, piece):
    for rule in rules:
        if rule[0] == '*':
            return(rule[1])
        elif rule[0] == '>':
            if piece[rule[2]] > rule[3]:
                return(rule[1])
        else:
            if piece[rule[2]] < rule[3]:
                return(rule[1])
    return(rules[-1][1])

def star1(workflows, ratings):
    star1 = 0
    accepted = []

    for piece in ratings:
        position = 'in'

        while not (position in ['A', 'R']):
            rules = workflows[position]
            position = applyRules(rules, piece)
            
        if position == 'A':
            accepted.append(piece)

    for piece in accepted:
        star1 += piece['x'] + piece['m'] + piece['a'] + piece['s']

    print(f"****** {Style.GREEN} First Star = {star1} {Style.RESET}")

def star2(workflows):
    star2 = 0
    accepted = []

    ranges = [['in', {'x':[1,4000], 'm':[1,4000], 'a':[1,4000], 's':[1,4000]}]]

    possible_pieces = {'A':[], 'R':[]}
    iteration = 0
    while len(ranges) > 0:
        current_range = ranges.pop()

        position = current_range[0]
        values = current_range[1]

        if position in ['A', 'R']:
            possible_pieces[position].append(values)
            continue

        rules = workflows[position]
        for rule in rules:
            ## applying 
            if rule[0] == '*':
                ## on envoie tout le range dans cette position
                current_range[0] = rule[1]
                ranges.append(current_range)
                break
            else:
                new_range = copy.deepcopy(current_range)
                destination = rule[1]
                cara = rule[2]
                borne = rule[3]
                intervalle = values[cara]
                result = split_interval(intervalle, borne)

                if rule[0] == '>':
                ## on regarde si on peut appliquer cette regle et on créer les intervalles associés
                    if len(result[1]) > 0:
                        ## on applique la relge au range qui sont au dessus
                        new_range[0] = destination
                        new_range[1][cara] = result[1]
                        new_range[1][cara][0] += 1
                        ranges.append(new_range)

                        ## on update le current range avec les valeurs qui sont en dessus pour le reste des regles
                        if len(result[0]) > 0:
                            current_range[1][cara] = result[0]

                else:
                    if len(result[0]) > 0:
                        ## on applique la relge au range qui sont au dessus
                        new_range[0] = destination
                        new_range[1][cara] = result[0]
                        new_range[1][cara][1] -= 1
                        ranges.append(new_range)
                        
                        ## on update le current range avec les valeurs qui sont en dessus pour le reste des regles
                        if len(result[1]) > 0:
                            current_range[1][cara] = result[1]

        iteration += 1
        
    for accepted_pieces in possible_pieces['A']:
        val = 1
        for ranges in accepted_pieces.values():
            val *= ranges[1]-ranges[0]+1

        star2 += val


    print(f"****** {Style.BLUE} Second Star = {star2} {Style.RESET}")  


fileToOpen = "./2023/Day19.txt"
workflows, ratings = readInstruction(fileToOpen)

star1(workflows, ratings)
star2(workflows)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 