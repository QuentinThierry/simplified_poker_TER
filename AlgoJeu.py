from random import randrange
import matplotlib.pyplot as plt

from tqdm import tqdm
import time

# 0 : lay down, 1 : bet 1€, 2 : bet 3€
def alice_bet(alice_money):
    x = randrange(0,3)
    if x == 2:
        x = 3
    
    if (alice_money - x) >= 0:
        return x
    else:
        if (alice_money - 1) <= -1:
            return 0
        else:
            return 1

# 0 : lay down, 1 : follow alice
def bob_bet():
    return randrange(0,2)
    

start = 0
end = 0

res = []

iterations = 1000

for i in tqdm(range(iterations)):
    start += time.time()
    
    alice_money = 100
    bob_money = 100
    alice_bet_amount = 0
    total_bet = 0

    while alice_money > 0 and bob_money > 0:
        
        # random card draw
        alice_card = randrange(1,11)
        
        alice_bet_amount = alice_bet(alice_money)

        if alice_bet_amount != 0: # if alice doesnt lay down
            total_bet += alice_bet_amount # add alice bet to total
            alice_money -= alice_bet_amount
            bob_card = randrange(1,11)
            
            if bob_bet() != 0: # if bob doesnt lay down
                total_bet += alice_bet_amount
                bob_money -= alice_bet_amount
                if bob_money < 0:
                    total_bet += bob_money
                    bob_money = 0

                if alice_card > bob_card: # alice wins
                    alice_money += total_bet
                    total_bet = 0
                    
                elif alice_card < bob_card: # bob wins
                    bob_money += total_bet
                    total_bet = 0
            else:
                alice_money += total_bet
                total_bet = 0
        else:
            bob_money += total_bet
            total_bet = 0
            
    end += time.time()
    
    if alice_money <= 0:
        res.append("Bob")
    else:
        res.append("Alice")


value_a = res.count("Alice")
value_b = res.count("Bob")

values = [value_a, value_b]
names = ['Alice', 'Bob']

plt.bar(names, values)
plt.show()

print("Alice won", value_a, "times.")
print("Bob won", value_b, "times.")
print("Number of games :", iterations)
print("Average time of one game :", round((end - start)/iterations, 5), 's')

