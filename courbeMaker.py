import matplotlib.pyplot as plt
import numpy as np 

def makeCurves(nbValues, f, ab, aliceAct, title):
    
    if ab:
        array0 = [1/3]
        array1 = [1/3]
        array2 = [1/3]

    else:
        array0 = [1/2]
        array1 = [1/2]
        if aliceAct:
            col = "orange" #3
        else:
            col = "deeppink" #1

    line = f.readline()

    xCmpt = 0
    
    while line:

        xCmpt += 1

        if xCmpt >= nbValues:
            break

        i = 0
        for splt_line in line.split(" "):
            if i == 0:
                array0.append(float(splt_line))
            elif i == 1:
                array1.append(float(splt_line))
            elif i == 2:
                array2.append(float(splt_line))
            i += 1

        line = f.readline()

    if ab:
        plt.plot(array0, label="Passer", color="royalblue")
        plt.plot(array1, label="Miser 1", color="deeppink")
        plt.plot(array2, label="Miser 3", color="orange")
    
    else:
        plt.plot(array0, label="Passer", color="royalblue")
        plt.plot(array1, label="Suivre", color=col)

    plt.title(title)
    plt.legend()
    plt.show()


def makeHist(bluff_alice, bob_counter_bluff):
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.1,0.8,0.8])
    
    axis = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    
    x = np.arange(len(axis))
    width = 0.35
    
    ax.bar(x - width/2, bluff_alice, width, label='Bluff Alice')
    ax.bar(x + width/2, bob_counter_bluff, width, label='Contre-Bluff Bob (carte ∈ [1,6])')
    ax.set_xlabel('Carte Alice')
    ax.set_ylabel('Nombre de bluff')
    
    ax.set_xticklabels(axis)
    ax.set_xticks(x)
    
    ax.legend()
    
    plt.show()