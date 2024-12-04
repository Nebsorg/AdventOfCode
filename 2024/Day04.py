from datetime import datetime

#### Main
print(f"2024 --- Day 4: Ceres Search ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instructions = []
    for line in f:
        line = line.rstrip()
        instructions.append(line)
    return(instructions)

def exploreXMAS(i,j,word,pos, shifts, instructions):
    result= 0
    max_line = len(instructions)
    max_col = len(instructions[0])

    ## checking directions in shifts 
    for shift in shifts:
        new_i = i + shift[0]
        new_j = j + shift[1]
        if (0 <= new_i < max_line) and (0 <= new_j < max_col):
            if instructions[new_i][new_j] == word[pos]:
                if pos == len(word)-1:
                    return(1)
                else:
                    result += exploreXMAS(new_i, new_j, word, pos+1, [shift], instructions)
    return(result)

def exploreMAS(i,j,instructions):
    max_line = len(instructions)
    max_col = len(instructions[0])

    if i == 0 or i == max_line-1 or j == 0 or j == max_col-1:
        return(0)

    ## testing the MAS around : 
    if ( ((instructions[i-1][j-1] == 'M' and instructions[i+1][j+1] == 'S') or (instructions[i-1][j-1] == 'S' and instructions[i+1][j+1] == 'M')) 
        and ((instructions[i+1][j-1] == 'M' and instructions[i-1][j+1] == 'S') or (instructions[i+1][j-1] == 'S' and instructions[i-1][j+1] == 'M'))):
        return(1)
    
    return(0)

def stars(instructions):
    star1 = 0
    star2 = 0
    word = list("XMAS")
    shifts = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

    for i in range(len(instructions)):
        for j in range(len(instructions[i])):
            if instructions[i][j] == 'X':
                star1 += exploreXMAS(i,j,word,1, shifts, instructions)
            if instructions[i][j] == 'A':
                star2 += exploreMAS(i,j,instructions)

            
    print(f"****** First Star = {star1}")
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day04.txt"
instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 