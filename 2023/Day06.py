from datetime import datetime
import math

#### Main
print("2023 --- Day 6: Wait For It ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    ## read all instruction : 
    instruction_star1 = []
    instruction_star2 = []
    for i, line in enumerate(f):
        line = line.rstrip()
            
        if i == 0: 
            ref_times_star1 = list(map(int,line.split(':')[1].split()))
            ref_times_star2 = [int(line.split(':')[1].replace(" ", ""))]
        elif i == 1:
            ref_distances_star1 = list(map(int,line.split(':')[1].split()))
            ref_distances_star2 = [int(line.split(':')[1].replace(" ", ""))]

    return([ref_times_star1, ref_distances_star1], [ref_times_star2, ref_distances_star2])

def star(refs, starID):

    success = []
    for i in range(len(refs[0])):
        t_max = refs[0][i]
        d_max = refs[1][i]

        local_success = []
        for t in range(t_max):
            d = t*(t_max-t)
            if d > d_max:
                local_success.append(t)
                    
        #print(f"course {i} : len = {len(local_success)} -- success = {local_success}")
        success.append(len(local_success))

    print(f"****** {starID} Star = {math.prod(success)}")

fileToOpen = "./2023/Day06.txt"

refs_star1, refs_star2 = readInstruction(fileToOpen)

star(refs_star1, 'First')
star(refs_star2, 'Second')

# star(ref_times, ref_distances, 'First')

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 