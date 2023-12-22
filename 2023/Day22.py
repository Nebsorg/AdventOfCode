from datetime import datetime
from tools import Style
from tools import interval_intersection
import json

#### Main
print(f"{Style.RED}2023 --- Day 22: Sand Slabs ---{Style.RESET}")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")

    bricks = {}
    for i, line in enumerate(f):
        x1,y1,z1 = list(map(int,line.split('~')[0].split(',')))
        x2,y2,z2 = list(map(int,line.split('~')[1].split(',')))
        bricks[str(i+1)] = [x1,x2,y1,y2,z1,z2]

    return(bricks)



def fallBrick(id, bricks):
    stabilized = False
    x1,x2,y1,y2,z1,z2 = bricks[id]
   
    current_z = z1
   
    while not stabilized:
        ## checking below : 
        if current_z == 1: 
            return(current_z)
        
        ## is there bricks below: 
        below_bricks = [id for id,b in bricks.items() if b[5] == (current_z-1)]
        if len(below_bricks) > 0 : 
            for subbrick in below_bricks:
                sb_x1, sb_x2, sb_y1, sb_y2, sb_z1, sb_z2 = bricks[subbrick]

                if len(interval_intersection([x1, x2], [sb_x1, sb_x2]))>0 and len(interval_intersection([y1,y2], [sb_y1, sb_y2]))>0:
                    return(current_z)
            current_z -= 1
        else:
            current_z -= 1

def stabilize(bricks):
    bottom_levels = set([b[4] for b in bricks.values()])

    fallenbricks = []

    ## stabilizing all the bricks
    for level in bottom_levels:
        level_bricks = [id for id,b in bricks.items() if b[4] == level]
        #print(f"Treating bricks on level {level} : {level_bricks}")
        for brick in level_bricks:
            realBrick = bricks[brick]
            z1 = realBrick[4]
            z2 = realBrick[5]
            high = z2-z1
            new_z = fallBrick(brick, bricks)
            if new_z != z1:
                fallenbricks.append(brick)
            realBrick[4] = new_z
            realBrick[5] = new_z+high
    return(fallenbricks)

def stars(bricks):
    star1 = 0
    star2 = 0

    fallenbricks = stabilize(bricks)

    save_world = json.dumps(bricks)

    for id, realbrick in bricks.items():
        without = json.loads(save_world)
        del without[id]

        fallenbricks = stabilize(without)
        star2 += len(fallenbricks)
        if len(fallenbricks) == 0:
            star1 += 1

    print(f"****** {Style.GREEN} First Star = {star1} {Style.RESET}")
    print(f"****** {Style.BLUE} Second Star = {star2} {Style.RESET}")  


fileToOpen = "./2023/Day22.txt"
bricks = readInstruction(fileToOpen)

stars(bricks)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 