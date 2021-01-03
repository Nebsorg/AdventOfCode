from datetime import datetime
import copy

def score(hand):
    total = 0
    for i in range(len(hand)):
        total += hand[i] * (len(hand)-i)
    return(total)

def star1(hands):
        round = 1
        p1 = hands[1]
        p2 = hands[2]
        while len(p1)>0 and len(p2)>0:
            ## play first card:
            c1 = p1.pop(0)
            c2 = p2.pop(0)
            if c1 > c2:
                p1+=[c1,c2]
            else:
                p2+=[c2,c1]
            #print(f"#{round} : c1={c1} - c2={c2} - p1={p1} - p2={p2}")
            round += 1

        if len(p1) == 0:
            print("P2 win")
            return(score(p2))
        else:
            print("P1 win")
            return(score(p1))

def recursiveGame(p1, p2, gameId):
    print(f"=== Game {gameId} ===")
    round = 1
    p1History = []
    p2History = []

    while len(p1)>0 and len(p2)>0:
        print(f"-- Round {round} (Game {gameId}) --")
        print(f"Player 1's deck: {p1}")
        print(f"Player 2's deck: {p2}")
        if (p1 in p1History) or (p2 in p2History):
            print(f"Then winner of game {gameId} is player 1 (deck history)")
            return(1, score(p1))

        p1History.append(copy.deepcopy(p1))
        p2History.append(copy.deepcopy(p2))
        c1 = p1.pop(0)
        c2 = p2.pop(0)
        print(f"Player 1 plays: {c1}")
        print(f"Player 2 plays: {c2}")

        if (c1 <= len(p1)) and (c2 <= len(p2)):
            ## playing recursive game
            print(f"Playing a sub-game to determine the winner...")
            roundWinner, scoreWinner = recursiveGame(copy.deepcopy(p1[:c1]), copy.deepcopy(p2[:c2]), gameId+1)
            print(f"...anyway, back to game {gameId}.")
            if roundWinner == 1:
                print(f"Player 1 wins round {round} of game {gameId}!")
                p1+=[c1,c2]
            else:
                print(f"Player 2 wins round {round} of game {gameId}!")
                p2+=[c2,c1]
        else:
            if c1 > c2:
                print(f"Player 1 wins round {round} of game {gameId}!")
                p1+=[c1,c2]
            else:
                print(f"Player 2 wins round {round} of game {gameId}!")
                p2+=[c2,c1]
        round += 1
    if len(p1) == 0:
        print(f"Then winner of game {gameId} is player 2 (standard)")
        return(2, score(p2))
    else:
        print(f"Then winner of game {gameId} is player 1 (standard)")
        return(1, score(p1))

def star2(hands):
    gameId = 1
    winner, score = recursiveGame(hands[1], hands[2], gameId)
    return(score)



if __name__ == '__main__':
    start_time = datetime.now()
    f = open("Z:\donnees\developpement\Python\AdventOfCode\day22.txt", "r")
    hands = {}
    hands[1]=[]
    hands[2]=[]
    player = 0
    for line in f:
        line = line.rstrip("\n")
        if ':' in line:
            player += 1
        elif line != "":
            hands[player].append(int(line))
    f.close()
    handsStar2 = copy.deepcopy(hands)
    print(f"star1 = {star1(hands)}")
    print(f"star2 = {star2(handsStar2)}")

    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
