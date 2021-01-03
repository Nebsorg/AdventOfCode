from datetime import datetime


def loop(input, subjectNb):
    value = input * subjectNb
    value = value % 20201227
    return(value)

def loops(subjectNb, nbLoop):
    result = 1
    for i in range(nbLoop):
        result = loop(result, subjectNb)
    return(result)

def bruteForce(cardPublicKey, doorPublicKey):
    cardLoop = -1
    doorLoop = -1

    loopID = 1
    currentValue = 1
    print(f"Brute Force - card PK={cardPublicKey} - doorPK={doorPublicKey}")
    while cardLoop < 0 or doorLoop < 0:
        currentValue = loop(currentValue, 7)

        if currentValue == cardPublicKey:
            cardLoop = loopID
        if currentValue == doorPublicKey:
            doorLoop = loopID
        loopID += 1

    return(cardLoop, doorLoop)

def star1(inputs):
    initialSubjectNumber = 7
    cardPublicKey = inputs[0]
    doorPublicKey = inputs[1]

    cardLoop, doorLoop = bruteForce(cardPublicKey, doorPublicKey)
    print(f"Card Loop : {cardLoop} - Door Loop : {doorLoop}")

    ## calculate Encryption Key with min loops
    if cardLoop <= doorLoop:
        print(f"Calculate Encryption Key with Card Info : Door PK={doorPublicKey} - Card Loop : {cardLoop}")
        encryptionKey = loops(doorPublicKey, cardLoop)
    else:
        print(f"Calculate Encryption Key with Door Info : Card PK={cardPublicKey} - Door Loop : {doorLoop}")
        encryptionKey = loops(cardPublicKey, doorLoop)
    print(f"EncryptionKey = {encryptionKey}")

if __name__ == '__main__':
    start_time = datetime.now()
    inputTest = [5764801, 17807724]
    inputReal = [10212254, 12577395]

    star1(inputReal)

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
