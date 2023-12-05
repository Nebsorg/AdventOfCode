from datetime import datetime
from tools import *
import copy

#### Main
print("2023 --- Day 5: If You Give A Seed A Fertilizer ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instructions = {}
    initial_seeds_star1 = []
    initial_seeds_star2 = []
    depth = -1
    for i, line in enumerate(f):
        line = line.rstrip()
            
        if i == 0: 
            numbers = list(map(int,line.split(':')[1].split()))
           
            for number in numbers:
                initial_seeds_star1.append([number, number])          

            for i in range(0, len(numbers), 2):
                initial_seeds_star2.append([numbers[i], numbers[i]+numbers[i+1]-1])                
            continue

        if line == '':
            continue

        if "map:" in line:
            depth += 1
            instructions[depth] = []
            continue
        
        numbers = list(map(int,line.split()))
        instructions[depth].append(numbers)

    return(instructions, initial_seeds_star1, initial_seeds_star2)

def star(initial_seeds, instructions, starID):
    levels = instructions.keys()
    current_seeds = copy.deepcopy(initial_seeds)
    for i, level in enumerate(levels): 
        # print(f"level {i} starting with {len(current_seeds)} seeds")
        level_matches = instructions[level]
        new_seeds = []
        for rule in level_matches:
            # print(f"level {i} : applying rule {rule} to {current_seeds}")
            rule_seeds = copy.deepcopy(current_seeds)
            while (len(rule_seeds) > 0):
                seed = rule_seeds.pop()
                # print(f"level {i} : checking rule {rule} on seed {seed}")

                ## Is there an intersection with the current mapping ?
                mapping_range_min = rule[1]
                mapping_range_max = rule[1] + rule[2] - 1
                intersection = interval_intersection(seed,[mapping_range_min,mapping_range_max])

                if len(intersection) > 0:
                    #print(f"  --> Intersection found {intersection} on seed {seed} and rule {[mapping_range_min,mapping_range_max]}")
                    ## intersection found, treating this intersection : 
                    #       - remove current seed from list of seed
                    #       - adding transformed part to new seed
                    #       - add untouched part of current seed in list of seed
                    current_seeds.remove(seed)
                    ## applying the transformation to the intersection : 
                    new_min = intersection[0] - (rule[1] - rule[0])
                    new_max = intersection[1] - (rule[1] - rule[0])
                    new_seeds.append([new_min, new_max])
                    #print(f"  --> Transforming intersection {intersection} in {[new_min, new_max]}")

                    ## if some part of the seed range is not touched by the rule, adding to the seed to check for the rest of rules
                    new_intervals = cut_interval_with_interval(seed,[mapping_range_min,mapping_range_max])
                    for interval in new_intervals:
                        if interval != intersection:
                            current_seeds.append(interval)
                            #print(f"  --> Adding untransformed part of seed {seed} to seed to check {interval}")
                    

        ## once all the rules have been applied, adding remaining seed of current seed to new seeds
        #print(f"  --> Adding untransformed seed to next level {current_seeds}")
        new_seeds.extend(current_seeds)
        
        current_seeds = copy.deepcopy(new_seeds)
        #print(f"level {i} completed : new seed={len(current_seeds)}")

    borne_inf = min([d[0] for d in current_seeds])
    print(f"****** {starID} Star = {borne_inf}")


fileToOpen = "./2023/Day05.txt"

instructions, initial_seeds_star1, initial_seeds_star2 = readInstruction(fileToOpen)

star(initial_seeds_star1, instructions, 'First')
star(initial_seeds_star2, instructions, 'Second')

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 