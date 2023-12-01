from datetime import datetime

def star(input, NbOfRound):
    saidNumbers = {}
    firstTimeStr = ""

    for i in range(1, NbOfRound+1):
        if i in range(1, len(input)+1):
            ## we start by saying the input number and add them as "sayed on round i"
            lastNumberSaid = input[i-1]
            saidNumbers[lastNumberSaid] = [i,0]
        else:
            ## Cheking last nomber history : is it said for the first time ?
            nbHistory = saidNumbers[lastNumberSaid]
            if nbHistory[1] == 0:
                ## it was said for the first time
                numberToSay = 0
            else:
                numberToSay = nbHistory[0] - nbHistory[1]

            ## adding the number to say to history
            try:
                saidNumbers[numberToSay] = (i, saidNumbers[numberToSay][0])
            except KeyError:
                saidNumbers[numberToSay] = (i,0)

            lastNumberSaid = numberToSay
        #print(f"Round {i} - Number said = {lastNumberSaid}- {saidNumbers}")
    return(lastNumberSaid)

if __name__ == '__main__':
    start_time = datetime.now()
    input = [8,13,1,0,18,9]

    print(f"Star1 = {star(input, 2020)}")
    print(f"Star2 = {star(input, 30000000)}")
    ##Duration
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
