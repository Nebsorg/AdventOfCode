from datetime import datetime

#### Main
print(f"2024 --- Day 9: Disk Fragmenter ---")
start_time = datetime.now()

def readInstruction(file):
    f = open(file, "r")
    instructions = []
    ## read all instruction : 

    for line in f:
        line = line.rstrip()
        instructions.append(line)

    return(instructions)

def expend(disk):
    expended_disk = {}
    currentID = 0
    currentPos = 0
    for i, space in enumerate(disk):
        if i%2 == 0:
            id_to_add = currentID
            currentID += 1
        else:
            id_to_add = -1

        for j in range(int(space)):
            expended_disk[j+currentPos] = id_to_add
        currentPos += int(space)
    return(expended_disk)

def getLastPos(expended_disk, currentMin, currentMax):
    for i in range(currentMax-1, currentMin, -1):
        if expended_disk[i] != -1:
            return(i)
    return(currentMin)

def compact_star1(expended_disk):
    swp_pos = len(expended_disk)
    
    for i in range(len(expended_disk)):
        if expended_disk[i] == -1:
            swp_pos = getLastPos(expended_disk, i, swp_pos)
            expended_disk[i], expended_disk[swp_pos] = expended_disk[swp_pos], expended_disk[i]
    return(expended_disk)


def map_disk(expended):
    freeSpace = {}
    files = {}

    for disk_pos, file_id in expended.items():
        if disk_pos == 0:
            current = file_id
            start_current = 0
            len_current = 1
        else:
            if current != file_id:
                ## on change de zone
                if current == -1:
                    freeSpace[start_current] = len_current
                else:
                    files[current] = (start_current, len_current)
                current = file_id
                start_current = disk_pos
                len_current = 1
            else:
                len_current += 1
    if current == -1:
        freeSpace[start_current] = len_current
    else:
        files[current] = (start_current, len_current)

    return(freeSpace, files)

def compact_star2(expended_disk):
    max_id = max(expended_disk.values())

    for i in range(max_id, -1, -1):
        freespace, files = map_disk(expended_disk) ## strong improvement : don't remap disk at every cycle, but manage freespace manually

        file_position = files[i][0]
        size_to_found = files[i][1]
        
        for pos, size in freespace.items():
            if size_to_found <= size and pos < file_position:
                for k in range(size_to_found):
                    expended_disk[k+pos] = i
                    expended_disk[k+file_position] = -1
                break

    return(expended_disk)

def checksum(filesystem):
    chk = 0
    for pos, id in filesystem.items():
        if id != -1:
            chk += pos*id
    return(chk)

def stars(instructions):
    star1 = 0
    star2 = 0

    disk = instructions[0]

    ### Star 1
    expended = expend(disk)
    expended_star1 = expended.copy()
    compacted = compact_star1(expended_star1)
    star1 = checksum(compacted)
    print(f"****** First Star = {star1}")

    ### Star 2
    expended_star2 = expended.copy()
    compacted = compact_star2(expended_star2)
    star2 = checksum(compacted)
    print(f"****** Second Star = {star2}")  


fileToOpen = "./Day09.txt"
instructions = readInstruction(fileToOpen)
#print(instructions)

stars(instructions)

end_time = datetime.now()
print('\nDuration: {}'.format(end_time - start_time)) 