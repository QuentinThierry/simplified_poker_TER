import pstats
import cProfile
import random

from matplotlib.pyplot import title


import utils
import courbeMaker as cm

from tqdm import tqdm
import time

QALICE = [
    [1/3, 1/3, 1/3],  # 1
    [1/3, 1/3, 1/3],  # 2
    [1/3, 1/3, 1/3],  # 3
    [1/3, 1/3, 1/3],  # 4
    [1/3, 1/3, 1/3],  # 5
    [1/3, 1/3, 1/3],  # 6
    [1/3, 1/3, 1/3],  # 7
    [1/3, 1/3, 1/3],  # 8
    [1/3, 1/3, 1/3],  # 9
    [1/3, 1/3, 1/3]  # 10
]

QBOB = [
    # 1          #3
    [[1/2, 1/2], [1/2, 1/2]],  # 1
    [[1/2, 1/2], [1/2, 1/2]],  # 2
    [[1/2, 1/2], [1/2, 1/2]],  # 3
    [[1/2, 1/2], [1/2, 1/2]],  # 4
    [[1/2, 1/2], [1/2, 1/2]],  # 5
    [[1/2, 1/2], [1/2, 1/2]],  # 6
    [[1/2, 1/2], [1/2, 1/2]],  # 7
    [[1/2, 1/2], [1/2, 1/2]],  # 8
    [[1/2, 1/2], [1/2, 1/2]],  # 9
    [[1/2, 1/2], [1/2, 1/2]]  # 10
]


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
    # basics operations are faster than random.uniform for same result
    return (int(random.random() * 100) % 10) + 1


def take_action_alice(etat, Q, probExploration):
    # Take an random action
    rnd = random.random()
    if rnd < probExploration:
        action = (int(rnd * 100) % 3)

    else:  # Or greedy action
        rnd = random.random()
        if rnd <= Q[etat][0]:
            action = 0
        elif rnd <= (Q[etat][0] + Q[etat][1]):
            action = 1
        else:
            action = 2

    return action


def take_action_bob(etat, Q, choix_alice, probExploration):

    rnd = random.random()
    # Take an action
    if rnd < probExploration:
        action = (int(rnd * 100) % 2)
    else:  # Or greedy action
        rnd = random.random()
        if rnd <= Q[etat][choix_alice][0]:
            action = 0
        else:
            action = 1

    return action


bluff_alice = []
bob_counter_bluff = []

for i in range(10):
    bluff_alice.append(0)
    bob_counter_bluff.append(0)


def algo(alice_card, bob_card, alice_bet_amount, bob_bet_amount, pot_commun):

    pot_commun += 2

    # return works like : winner (A:0|B:1) | rA | rb | endValue

    # alice fold, rA = -1 | rB = 0
    if alice_bet_amount == 0:
        return 1, -1, 0, pot_commun

    # alice add her bet
    pot_commun += alice_bet_amount

    # bob fold good, rA = 1 | rB = -1
    # bob fold bad, rA = 1 | rB = -1
    if bob_bet_amount == 0:
        if alice_card > bob_card:
            return 0, 1, -1, pot_commun
        else:  # alice gagne alors qu'elle devait perdre (bluff)
            global bluff_alice
            bluff_alice[alice_card-1] += 1
            return 0, 1, -1, pot_commun

    # bob follows alice
    pot_commun += alice_bet_amount

    # alice wins, rA = mise+1 | rB = -(mise+1)
    if alice_card > bob_card:
        return 0, alice_bet_amount+1, -1*(alice_bet_amount+1), pot_commun

    # bob wins, rA = mise+1 | rB = -(mise+1)
    elif bob_card > alice_card:
        if bob_card <= 6:
            global bob_counter_bluff
            bob_counter_bluff[alice_card-1] += 1
        return 1, -1*(alice_bet_amount+1), alice_bet_amount+1, pot_commun

    # equality, rA = 0 | rB = 0
    else:
        return pot_commun, 0, 0, pot_commun


def afficher_table():

    for s in range(10):
        print(s+1, round(QALICE[s][0], 4),
              round(QALICE[s][1], 4), round(QALICE[s][2], 4))

    print("-----------------")

    for s in range(10):

        for x in range(2):
            print(s+1, round(QBOB[s][x][0], 4), round(QBOB[s][x][1], 4))
        print("\n")


def main():

    iterations = 1000000
    nbValues = 1000000
    print("START----------------------------------")
    print("Affichage des courbes des cartes 1 à 10 pour " + str(iterations) +
          " iterations et affichage de " + str(nbValues) + " valeurs.")
    for globi in range(0, 20):
        print("RUNNING itération :", globi, "FOR CARD :", int(globi/2) + 1)

        for x in range(10):
            for y in range(3):
                QALICE[x][y] = (1/3)
            for z in range(2):
                for a in range(2):
                    QBOB[x][z][a] = (1/2)

        start = 0
        end = 0

        everyN = round(iterations/nbValues) - 1

        if everyN == 0:
            everyN = 1

        res = []
        pot_commun = 0

        alice_money = 0
        bob_money = 0

        f = open("ResFile.txt", "w")

        f2 = open("ResFile2.txt", "w")

        f3 = open("ResFile3.txt", "w")

        for i in tqdm(range(1, iterations+1)):

            start += time.time()

            money = 0

            etatA = random_card()
            etatB = random_card()

            actionAliceIndice = 0

            if globi % 2 == 0:
                exploCoeff = 10000
            else:
                exploCoeff = 100000
            exploration = 1/((i/exploCoeff)+1)

            actA = take_action_alice(etatA-1, QALICE, exploration)

            if(actA == 0):
                actionAliceIndice = 0

            if(actA == 1):
                actionAliceIndice = 0

            else:  # 2
                actionAliceIndice = 1

            # prend l'état [etatB][x][0] de la table QBOB
            actB = take_action_bob(
                etatB-1, QBOB, actionAliceIndice, exploration)

            alice_bet_amount = choose_alice_action(actA)
            bob_bet_amount = choose_bob_action(actB)

            winner, rA, rB, money = algo(
                etatA, etatB, alice_bet_amount, bob_bet_amount, pot_commun)

            utils.change_proba_of_table(
                QALICE, etatA-1, actA, rA, actionAliceIndice)
            utils.change_proba_of_table(
                QBOB, etatB-1, actB, rB, actionAliceIndice)

            # Affichage
            if winner == 0:
                res.append("Alice")
                alice_money += money
                pot_commun = 0

            elif winner == 1:
                res.append("Bob")
                bob_money += money
                pot_commun = 0

            else:
                pot_commun = money

            x = int(globi/2)

            if (i % everyN == 0):
                f.write(str(round(QALICE[x][0], 3)) + " " + str(round(QALICE[x][1], 3)) + " " +
                        str(round(QALICE[x][2], 3)) + "\n")
                f2.write(str(round(QBOB[x][0][0], 3)) +
                         " " + str(round(QBOB[x][0][1], 3)) + "\n")
                f3.write(str(round(QBOB[x][1][0], 3)) +
                         " " + str(round(QBOB[x][1][1], 3)) + "\n")

            end += time.time()

        f.close()
        f2.close()
        f3.close()

        # Affichage

        # afficher_table()

        print("\nNumber of games :", iterations)
        print("Average time of one game :", round(
            (end - start)/iterations, 5), 's')

        value_a = res.count("Alice")
        value_b = res.count("Bob")

        print("Alice wins :", round(value_a/iterations, 4) * 100, "%")
        print("Bob wins :", round(value_b/iterations, 4) * 100, "%")
        print("Equality :", round(
            (iterations-(value_a+value_b))/iterations, 4) * 100, "%")

        print("Alice money : " + str(alice_money) + " (" +
              str(round(alice_money/(alice_money + bob_money)*100, 2)) + "%)")
        print("Bob money : " + str(bob_money) + " (" +
              str(round(bob_money/(alice_money + bob_money)*100, 2)) + "%)")

        print("Alice money average : " + str(round(alice_money/value_a, 2)))
        print("Bob money average : " + str(round(bob_money/value_b, 2)))

        # courbes par carte
        # Alice
        title = "Carte " + str(int(globi/2) + 1) + \
            " Alice (explo : " + str(exploCoeff) + ")"
        f = open("ResFile.txt", "r")
        cm.makeCurves(nbValues, f, 1, 0, title)

        title = "Carte " + str(int(globi/2) + 1) + \
            " Bob (explo : " + str(exploCoeff) + ")"
        # Bob 1
        f2 = open("ResFile2.txt", "r")
        cm.makeCurves(nbValues, f2, 0, 0, title)

        # Bob 2
        f3 = open("ResFile3.txt", "r")
        cm.makeCurves(nbValues, f3, 0, 1, title)

        # histogramme bluffs
        if globi == 0:
            cm.makeHist(bluff_alice, bob_counter_bluff)

        print(bob_counter_bluff)

        f.close()
        f2.close()
        f3.close()

    print("END----------------------------------")


# cProfile is used to debug complexity and get faster code.
cProfile.run('main()', "output.dat")

with open("output_time.txt", "w") as f:
    p = pstats.Stats("output.dat", stream=f)
    p.sort_stats("time").print_stats()

with open("output_calls.txt", "w") as f:
    p = pstats.Stats("output.dat", stream=f)
    p.sort_stats("calls").print_stats()
