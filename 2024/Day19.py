from datetime import datetime

#### Main
print(f"2024 --- Day 19: Linen Layout ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    designs = []
    for i,line in enumerate(f):
        line = line.rstrip()
        if i == 0:
            patterns = line.split(', ')
        elif i>1:
            designs.append(line)
    return([patterns, designs])

def calculateNbPossibilities(design, patterns, possibilityCount, memory, depth):
    ## calculate all possibility with memory to avoir recalculation. Not storing arrangement
    #print(f"|{depth}|{' '*4*depth} - TestPattern - {design=}, {possibilityCount=}")
    
    ## get all unknown part in the spring : 
    options = [pattern for pattern in patterns if pattern == design[0:len(pattern)]]

    if len(options) == 0:
        ## pas de solution
        #print(f"|{depth}|{' '*4*depth}      -> no option - end of execution returning 0")    
        return(0)

    #print(f"|{depth}|{' '*4*depth}      -> len(options)={len(options)}, {options=}")

    new_possibilityCount = 0
    for pattern in options: 
        sub_design = design[len(pattern):]
        if sub_design in memory:
            new_possibilityCount += memory[sub_design]
        else:
            if len(sub_design) > 0:
                #print(f"|{depth}|{' '*4*depth}      -> testing pattern {pattern} - subdesign={sub_design}")
                result = calculateNbPossibilities(sub_design, patterns, possibilityCount, memory, depth+1)
                #print(f"|{depth}|{' '*4*depth}      -> result of testPatters :{result}")    
                memory[sub_design] = result
                new_possibilityCount += result
            else:
                ## il ne reste plus rien
                new_possibilityCount += 1
                #print(f"|{depth}|{' '*4*depth}      -> dsub design empty - {possibilityCount=}")
    #print(f"|{depth}|{' '*4*depth}      -> End of execution - returning arrangements - {possibilityCount}")    
    return(new_possibilityCount)

def stars(instructions):
    star1 = 0
    star2 = 0

    patterns = instructions[0]
    designs = instructions[1]

    memory = {}
    for design in designs:
        possibilityCount = calculateNbPossibilities(design, patterns, 0, memory, 0)
        #print(f" - testing design Arrangement possibles for {design} - {possibilityCount}" )
        if possibilityCount > 0:
            star1+=1
        star2 += possibilityCount

    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  

fileToOpen = "./Day19.txt"

instructions = readInstruction(fileToOpen)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 