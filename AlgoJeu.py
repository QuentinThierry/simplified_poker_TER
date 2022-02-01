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

def take_action(etat, Q, probExploration):
    # Take an action
    if random.uniform(0, 1) < probExploration:
        action = randrange(0, 3)
    else: # Or greedy action
        action = np.argmax(Q[etat])
    return action

def def_bob_bet():
    return randrange(0,2)


def algo(alice_card, alice_bet_amount, alice_money, total_bet, bob_money, bob_bet):
    # random card draw
    
    bob_card = randrange(1,11)

    if alice_bet_amount != 0: # if alice doesnt lay down
        total_bet += alice_bet_amount # add alice bet to total
        alice_money -= alice_bet_amount
        
        if bob_bet != 0: # if bob doesnt lay down
            total_bet += alice_bet_amount
            bob_money -= alice_bet_amount
            if bob_money < 0:
                total_bet += bob_money
                bob_money = 0

            if alice_card > bob_card: # alice wins
                alice_money += total_bet
                total_bet = 0
                return 1, alice_money, bob_money, total_bet
                
            elif alice_card < bob_card: # bob wins
                bob_money += total_bet
                total_bet = 0
                return -1, alice_money, bob_money, total_bet
        else:
            alice_money += total_bet # alice wins by default -> bob lay down
            total_bet = 0
            if alice_card > bob_card: # alice wins
                return 1, alice_money, bob_money, total_bet
            else:
                return -1, alice_money, bob_money, total_bet
    else:
        bob_money += total_bet # alice loses by default -> alice lay down
        total_bet = 0
        if alice_card > bob_card: # alice wins
            return -1, alice_money, bob_money, total_bet
        else:
            return 1, alice_money, bob_money, total_bet
    
    return 0, alice_money, bob_money, total_bet


QALICE = [
    [0, 0, 0],   #0
    [0, 0, 0],   #1
    [0, 0, 0],   #2
    [0, 0, 0],   #3
    [0, 0, 0],   #4
    [0, 0, 0],   #5
    [0, 0, 0],   #6
    [0, 0, 0],   #7
    [0, 0, 0],   #8
    [0, 0, 0]    #9
]

start = 0
end = 0
iterations = 1000
res = []
iters = []
test = []

for i in tqdm(range(iterations)):
    
    alice_money = 100
    bob_money = 100
    alice_bet_amount = 0
    total_bet = 0
    start += time.time()

    while alice_money > 0 and bob_money > 0:
        
        etat = random_card()

        act = take_action(etat-1, QALICE, 0.1)

        alice_bet_amount = choose_alice_action(act)

        r, alice_money, bob_money, total_bet = algo(etat-1, alice_bet_amount, alice_money, total_bet, bob_money, def_bob_bet())
        
        QALICE[etat-1][act] = QALICE[etat-1][act] + 0.1*(r - QALICE[etat-1][act])
        
    if alice_money > bob_money:
        res.append("Alice")
        test.append(res.count("Alice"))
    else:
        res.append("Bob")
    
    iters.append(i)
    
    end += time.time()



def afficher_table():
    
    for s in range(0, 10):
        print(s+1, round(QALICE[s][0],4), round(QALICE[s][1],4), round(QALICE[s][2],4))

afficher_table()

print("Number of games :", iterations)
print("Average time of one game :", round((end - start)/iterations, 5), 's')

value_a = res.count("Alice")
value_b = res.count("Bob")


print("Alice wins :", value_a)
print("Bob wins :", value_b)

plt.scatter(iters , test, c="r", cmap='summer')
plt.show()
