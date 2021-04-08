from random import *
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt

ansa = 2
ansb = -1

points = []

lst = list(range(0,12))    
comb = list(combinations(lst, 6))
sz = len(comb)
global m
m=1

def fit():
    global m
    rr = np.random.normal(0,2,12)
    points.clear()
    for i in range(0, 12):
        x = i-5
        y = (x, 2*x - 1 + rr[i])
        points.append(y)
    #RANSAC
    errora = 100 
    errorb = 100
    x = []
    y = []
    while(errora > 5 or errorb > 5):
        n = randint(0, sz-1)

        A = np.zeros((6,2))
        B = np.zeros((6,1))
        x.clear()
        y.clear()
        for i in range(0,6):
            A[i][0] = points[comb[n][i]][0]
            x.append(A[i][0])
            A[i][1] = 1
            B[i][0] = points[comb[n][i]][1]
            y.append(B[i][0])
        v = np.linalg.pinv(A) @ B
        errora = abs((ansa-v[0][0])/ansa)*100
        errorb = abs((ansb-v[1][0])/ansb)*100
    
    print("RANSAC: ")
    print(v)
    print(str(errora) + '%, ' + str(errorb) + '%\n')
    plt.subplot(1,2,1)
    plt.scatter(x,y)
    xx = np.arange(-5,6)
    yy = 2*xx-1
    plt.plot(xx, yy, color = 'b')
    ny = v[0][0]*xx + v[1][0]
    plt.plot(xx, ny, color = 'r')
    plt.axvline(x=0, color = 'g') 
    plt.axhline(y=0, color = 'g')
    plt.axis([-6.5, 6.5, -12, 12])
    plt.title('RANSAC')


    x.clear()
    y.clear()
    #ALL_FITTING
    C = np.zeros((12,2))
    D = np.zeros((12,1))
    for j in range(0,12):
        C[j][0] = points[j][0]
        C[j][1] = 1
        D[j][0] = points[j][1]
        x.append(C[j][0])
        y.append(D[j][0])
    u = np.linalg.pinv(C) @ D
    errorc = abs((ansa-u[0][0])/ansa)*100
    errord = abs((ansb-u[1][0])/ansb)*100
    print("ALL_FITTING: ")
    print(u)
    print(str(errorc) + '%, ' + str(errord) + '%\n---------------------------------------------')
    plt.subplot(1,2,2)
    plt.scatter(x,y)
    xx = np.arange(-5,6)
    yy = 2*xx-1
    plt.plot(xx, yy, color = 'b')
    ny = u[0][0]*xx + u[1][0]
    plt.plot(xx, ny, color = 'r')
    plt.axvline(x=0, color = 'g') 
    plt.axhline(y=0, color = 'g') 
    plt.axis([-6.5, 6.5, -12, 12])
    plt.title('ALL FITTING')
                
    plt.tight_layout
    plt.savefig('output/result' + str(m) + '.jpeg')
    plt.clf()
    m += 1

def main():
    for k in range(0,10):
        if(k == 0):
            print("1st Try: ")
        if(k == 1):
            print("2nd Try:")
        if(k>1):
            print(str(k+1) + "th Try:")
        fit()

if __name__ == "__main__":
    main()