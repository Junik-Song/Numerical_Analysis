import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
from random import *
import scipy.stats as stats
from sklearn.cluster import KMeans
from skimage import io
from sklearn.preprocessing import MinMaxScaler
from mpl_toolkits.mplot3d import Axes3D

# rr = np.random.normal(0,2,12)

num = 300
scaler = MinMaxScaler()
means = [[3,3,3], [5,1,-1], [2,5,5], [4,-3,-2], [0,2,-4], [-7,7,4]]
vars = [[3,2,5], [4,3,2], [2,4,2], [3,2,1], [1,3,5], [4,2,5]]


d_means = np.zeros((5,3))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Generating Clusters

for i in range(0,5):
    cltA = np.zeros((3, num))
    for j in range(0,3):
        cltA[j][:] = np.random.normal(means[i][j],vars[i][j],num)


    ax.scatter(cltA[0][:], cltA[1][:], cltA[2][:], linewidths = 0.1)

    # Use K-Means for each Clusters

    kA = KMeans(n_clusters = 3, max_iter=100).fit(cltA)
    labelA = kA.labels_
    centerA = kA.cluster_centers_

    for j in range(0,3):
        d_means[i][j] = np.mean(centerA[labelA[j],:])


# mean x = np.mean(center[label[0],:]) mean y: 0->1, mean z: 0->2
print(means)
print(d_means)


plt.savefig('output/resultA.jpeg')
plt.show()


acc = []

# Test 1 - Original means and var
max = -1     # Max Distance
for i in range(0,5):
    errs = np.zeros((5))
    #print(means)
    #print(d_means)
    print("Case " + str(i+1))
    test = np.zeros((3, 100))
    test[0][:] = np.random.normal(means[i][0],vars[i][0],100)
    test[1][:] = np.random.normal(means[i][1],vars[i][1],100)
    test[2][:] = np.random.normal(means[i][2],vars[i][2],100)
    
    accuracy = 0

    for j in range(0,100):
        dist = 10
        idx = -1
        for k in range(0,5):
            v = np.linalg.norm(test[:,j] - np.transpose(d_means[k,:]))
            if(max < v and v <= 10):
                max = v
            if(v < dist):
                idx = k
                dist = v
        errs[idx] += 1
        if(idx == i):  
            accuracy += 1
        if(idx != i and idx != -1):
            print("Wrong at" + str(test[:,j])+" Expected " + str(idx+1) + ", Answer is " + str(1+i))
        if(idx == -1):
            print("Wrong at" + str(test[:,j])+" Expected None, Answer is " + str(i+1))
            
    print("Accuracy = " + str(accuracy) + "%")
    acc.append(accuracy)
    print(errs)

    #input("Press Enter to Continue")

a = 10
b = []
# Test 2 - Completely Random Values
for w in range(0,10):
    max = a - w*0.5
    test = np.zeros((3, 100))
    test[0][:] = np.random.normal(means[5][0],vars[5][0],100)
    test[1][:] = np.random.normal(means[5][1],vars[5][1],100)
    test[2][:] = np.random.normal(means[5][2],vars[5][2],100)
    z = 0
    for j in range(0,100):
        dist = 100
        idx = -1
        for k in range(0,5):
            v = np.linalg.norm(test[:,j] - np.transpose(d_means[k,:]))
            if(v < dist and v <= max):
                idx = k
                dist = v
        if(idx == -1):
            print("Too Far " + str(test[:,j]))
        if(idx != -1):
            z+=1
            print("Expected " + str(idx+1)+ " "+ str(test[:,j]))
    b.append(z)

for i in range(0,5):
    print("Case " + str(i+1) + " Accuracy: " + str(acc[i]) + "%")
tmp = 0
for u in b:
    print("Case 6, Max=" + str(a-tmp*0.5)+ ": Expected None as Some Clusters: " + str(u) + "/100")
    
    tmp+=1



print("\n\n")





for i in range(0,6):
    print("#Case " + str(i+1) + ": X=N(" + str(means[i][0]) +"," + str(vars[i][0]) + "), Y=N(" 
          + str(means[i][1]) +"," + str(vars[i][1]) + "), Z=N("
          + str(means[i][2]) +"," + str(vars[i][2]) + ")")