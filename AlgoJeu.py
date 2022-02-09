from random import randrange
import random
import matplotlib.pyplot as plt
import numpy as np

from tqdm import tqdm
import time



def choose_alice_action(choice):
    
    if choice == 0:
        return 0
    elif choice == 1:
        return 1
    elif choice == 2:
        return 3
    else:
        print("error alice action")
        return 0

def choose_bob_action(choice):
    if choice == 0:
        return 0
    elif choice == 1:
        return 1
    else:
        print("error bob action")
        return 0


def random_card():
    return randrange(1,11)

def take_action_alice(etat, Q, probExploration):
    # Take an action
    if random.uniform(0, 1) < probExploration:
        action = randrange(0, 3)
    else: # Or greedy action
        action = np.argmax(Q[etat])
    return action

def take_action_bob(etat, Q, probExploration):
        # Take an action
    if random.uniform(0, 1) < probExploration:
        action = randrange(0, 2)
    else: # Or greedy action
        action = np.argmax(Q[etat])
    return action



def algo(alice_card, bob_card, alice_bet_amount, bob_bet_amount):
    
    global alice_money
    global bob_money
    global total_bet

    if alice_bet_amount != 0: # if alice doesnt lay down
        total_bet += alice_bet_amount # add alice bet to total
        alice_money -= alice_bet_amount
        
        if bob_bet_amount != 0: # if bob doesnt lay down
            total_bet += alice_bet_amount
            bob_money -= alice_bet_amount
            if bob_money < 0:
                total_bet += bob_money
                bob_money = 0

            if alice_card > bob_card: # alice wins
                alice_money += total_bet
                total_bet = 0
                return 1, -1
                
            elif alice_card < bob_card: # bob wins
                bob_money += total_bet
                total_bet = 0
                return -1, 1
        else:
            alice_money += total_bet # alice wins by default -> bob lay down
            total_bet = 0
            if alice_card > bob_card: # alice would have win, and she did
                return 1, 1
            else:                      # bob lay down, and win
                return -1, -1
    else:
        bob_money += total_bet # alice loses by default -> alice lay down
        total_bet = 0
        if alice_card > bob_card: # alice would have win, and she didnt
            return -1, 0
        else:
            return 1, 0
    
    return 0, 0


QALICE = [
    [0, 0, 0],   #1
    [0, 0, 0],   #2
    [0, 0, 0],   #3
    [0, 0, 0],   #4
    [0, 0, 0],   #5
    [0, 0, 0],   #6
    [0, 0, 0],   #7
    [0, 0, 0],   #8
    [0, 0, 0],   #9
    [0, 0, 0]    #10
]

QBOB = [
    [0, 0],   #1
    [0, 0],   #2
    [0, 0],   #3
    [0, 0],   #4
    [0, 0],   #5
    [0, 0],   #6
    [0, 0],   #7
    [0, 0],   #8
    [0, 0],   #9
    [0, 0]    #10
]

start = 0
end = 0
iterations = 1000
res = []

for i in tqdm(range(iterations)):
    
    alice_money = 100
    bob_money = 100
    alice_bet_amount = 0
    bob_bet_amount = 0
    total_bet = 0
    start += time.time()

    while alice_money > 0 and bob_money > 0:
        
        etatA = random_card()
        etatB = random_card()

        actA = take_action_alice(etatA-1, QALICE, 0.1)
        actB = take_action_bob(etatB-1, QBOB, 0.1)

        alice_bet_amount = choose_alice_action(actA)
        bob_bet_amount = choose_bob_action(actB)
        
        rA, rB = algo(etatA, etatB, alice_bet_amount, bob_bet_amount)
        
        QALICE[etatA-1][actA] = QALICE[etatA-1][actA] + 0.1*(rA - QALICE[etatA-1][actA])
        QBOB[etatB-1][actB] = QBOB[etatB-1][actB] + 0.1*(rB - QBOB[etatB-1][actB])
    
    if alice_money > bob_money:
        res.append("Alice")
    else:
        res.append("Bob")
    
    end += time.time()





def afficher_table():
    
    for s in range(0, 10):
        print(s+1, round(QALICE[s][0],4), round(QALICE[s][1],4), round(QALICE[s][2],4))
    
    print("-----------------")
    
    for s in range(0, 10):
        print(s+1, round(QBOB[s][0],4), round(QBOB[s][1],4))
    

afficher_table()

print("Number of games :", iterations)
print("Average time of one game :", round((end - start)/iterations, 5), 's')

value_a = res.count("Alice")
value_b = res.count("Bob")


print("Alice wins :", value_a)
print("Bob wins :", value_b)
