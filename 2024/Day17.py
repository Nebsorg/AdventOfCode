from datetime import datetime

#### Main
print(f"2024 --- Day 17: Chronospatial Computer ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    for i,line in enumerate(f):
        line = line.rstrip()
        if i == 0:
            reg_a = int(line[12:])
        elif i == 1:
            reg_b = int(line[12:])
        elif i == 2:
            reg_c = int(line[12:])
        elif i == 4:
            program = [int(x) for x in line[8:].split(',')]
    return([reg_a, reg_b, reg_c, program])

def executeProgram(reg_a, reg_b, reg_c, program):
    position = 0
    finished = False
    output = []
    while not finished:
        opcode = program[position]
        if position + 1 >= len(program):
            return(reg_a, reg_b, reg_c, output)
        lit_operand = program[position+1]
        if lit_operand < 4:
            combo_operand = lit_operand
        elif lit_operand == 4:
            combo_operand = reg_a
        elif lit_operand == 5:
            combo_operand = reg_b
        elif lit_operand == 6:
            combo_operand = reg_c
        elif lit_operand == 7:
            if opcode in [0,2,5]:
                return(reg_a, reg_b, reg_c, output)
            combo_operand = lit_operand
        #print(f"current position = {position} - {opcode=}, {lit_operand=}, {combo_operand=}")
        match opcode:
            case 0:
                ## ADV - numerator = reg_a, denominator = 2^combo_op
                reg_a = int(reg_a/pow(2,combo_operand))
                position += 2
            case 1:
                ## BLX - reg_b = xor(reg_b, lit_op)
                reg_b = reg_b ^ lit_operand
                position += 2
            case 2:
                ## bst  - reb_b = comb%8
                reg_b = combo_operand % 8
                position += 2
            case 3:
                ## jnz - nothing si a=0, sinon jump to literal
                if reg_a == 0:
                    position +=2
                else:
                    position = lit_operand
            case 4:
                ## bxc : xor(b,c)
                reg_b = reg_b ^ reg_c
                position +=2
            case 5:
                ## out : combo%8, output it
                output.append(combo_operand%8)
                position +=2
            case 6:
                ## BDV - numerator = reg_a, denominator = 2^combo_op
                reg_b = int(reg_a/pow(2,combo_operand))
                position += 2
            case 7:
                ## CDV - numerator = reg_a, denominator = 2^combo_op
                reg_c = int(reg_a/pow(2,combo_operand))
                position += 2

        if position >= len(program):
            return(reg_a, reg_b, reg_c, output)
    return(reg_a, reg_b, reg_c, output)


def getDigits(reg_a,reg_b,reg_c,program, depth):
    ## Le system reponds à une logique de puissance de 8. 
    ## chaque modulo 8 renvoie un digit supplementaire
    ## il faut donc trouver tous les digits par pas de 8

    candidates = []
    for a in range(8):
        _,_,_, output = executeProgram(reg_a+a, reg_b, reg_c, program)
        if output == program[-depth-1:]:
                ## cette valeur de a match la fin du program
                candidates.append(reg_a+a)    
    
    if len(candidates) == 0:
        ## aucune valeur n'a matché, c'est une impasse
        return(-1)

    ## on a des candidats, on les inspectes : 

    
    if depth == len(program)-1:
        ## on a couvert tout le programme, on renvoie le meilleur candidat
        return(min(candidates))

    ## on explore un cran plus bas et on renvoie le meilleur
    bestCandidate = []
    for candidate in candidates:
        new_reg_a = getDigits(candidate*8, reg_b, reg_c, program, depth+1)
        if new_reg_a != -1:
            bestCandidate.append(new_reg_a)

    if len(bestCandidate) > 0:
        return(min(bestCandidate))
    else:
        return(-1)
        

def stars(instructions):
    star1 = 0
    star2 = 0

    reg_a = instructions[0]
    reg_b = instructions[1]
    reg_c = instructions[2]
    program = instructions[3]

    _, _, _, output = executeProgram(reg_a, reg_b, reg_c, program)
    star1 = ','.join([str(x) for x in output])
    print(f"****** First Star = {star1}")

    reg_a = instructions[0]
    reg_b = instructions[1]
    reg_c = instructions[2]
    program = instructions[3]
    star2 = getDigits(0,reg_b,reg_c, program, 0)
    print(f"****** Second Star = {star2}")  

fileToOpen = "./Day17.txt"

instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 