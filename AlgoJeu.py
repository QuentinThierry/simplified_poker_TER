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

def algo(alice_card, alice_bet_amount, alice_money, total_bet, bob_money, bob_bet=1):
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
                return 1
                
            elif alice_card < bob_card: # bob wins
                bob_money += total_bet
                total_bet = 0
                return -1
        else:
            alice_money += total_bet # alice wins by default -> bob lay down
            total_bet = 0
            if alice_card > bob_card: # alice wins
                return 1
            else:
                return -1
    else:
        bob_money += total_bet # alice loses by default -> alice lay down
        total_bet = 0
        if alice_card > bob_card: # alice wins
            return -1
        else:
            return 1
    
    return 0



QALICE = [
    [-1, 0, 0],   #0
    [-1, 0, 0],   #1
    [-1, 0, 0],   #2
    [-1, 0, 0],   #3
    [-1, 0, 0],   #4
    [-1, 0, 0],   #5
    [-1, 0, 0],   #6
    [-1, 0, 0],   #7
    [-1, 0, 0],   #8
    [-1, 0, 0]    #9
]


alice_money = 100
bob_money = 100
alice_bet_amount = 0
total_bet = 0

for _ in tqdm(range(100000000)):
    etat = random_card()

    act = take_action(etat-1, QALICE, 0.01)

    alice_bet_amount = choose_alice_action(act)

    r = algo(etat-1, alice_bet_amount, alice_money, total_bet, bob_money)

    QALICE[etat-1][act] = QALICE[etat-1][act] + 0.1*(r - QALICE[etat-1][act])

def afficher_table():
    
    for s in range(0, 10):
        print(s, round(QALICE[s][0],4), round(QALICE[s][1],4), round(QALICE[s][2],4))

afficher_table()





# # 0 : lay down, 1 : bet 1€, 2 : bet 3€
# def alice_bet(alice_money):
#     x = randrange(0,3)
#     if x == 2:
#         x = 3
    
#     if (alice_money - x) >= 0:
#         return x
#     else:
#         if (alice_money - 1) <= -1:
#             return 0
#         else:
#             return 1

# # 0 : lay down, 1 : follow alice
# def bob_bet():
#     return randrange(0,2)
    

# start = 0
# end = 0

# res = []

# iterations = 1000

# for i in tqdm(range(iterations)):
#     start += time.time()
    
#     alice_money = 100
#     bob_money = 100
#     alice_bet_amount = 0
#     total_bet = 0

#     while alice_money > 0 and bob_money > 0:
        
#         # random card draw
#         alice_card = randrange(1,11)
        
#         alice_bet_amount = alice_bet(alice_money)

#         if alice_bet_amount != 0: # if alice doesnt lay down
#             total_bet += alice_bet_amount # add alice bet to total
#             alice_money -= alice_bet_amount
#             bob_card = randrange(1,11)
            
#             if bob_bet() != 0: # if bob doesnt lay down
#                 total_bet += alice_bet_amount
#                 bob_money -= alice_bet_amount
#                 if bob_money < 0:
#                     total_bet += bob_money
#                     bob_money = 0

#                 if alice_card > bob_card: # alice wins
#                     alice_money += total_bet
#                     total_bet = 0
                    
#                 elif alice_card < bob_card: # bob wins
#                     bob_money += total_bet
#                     total_bet = 0
#             else:
#                 alice_money += total_bet
#                 total_bet = 0
#         else:
#             bob_money += total_bet
#             total_bet = 0
            
#     end += time.time()
    
#     if alice_money <= 0:
#         res.append("Bob")
#     else:
#         res.append("Alice")


# value_a = res.count("Alice")
# value_b = res.count("Bob")

# values = [value_a, value_b]
# names = ['Alice', 'Bob']

# plt.bar(names, values)
# plt.show()

# print("Alice won", value_a, "times.")
# print("Bob won", value_b, "times.")
# print("Number of games :", iterations)
# print("Average time of one game :", round((end - start)/iterations, 5), 's')

