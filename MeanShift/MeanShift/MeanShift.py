import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
from random import *
import scipy.stats as stats
from sklearn.cluster import MeanShift
from sklearn.cluster import KMeans
from skimage.color import rgb2lab
from skimage.color import lab2rgb
from skimage import io

# 0: Mean Shift, 1: K-Means
clt = 1

pic = True
coord = True

IMG = []

width = 640
height = 360

m=1

x=4
y=64
z=128

def makeMShift(im, num):
    print("Start")
    newLab = MeanShift(bandwidth = num, bin_seeding = True, max_iter = 100).fit(im)
    label = newLab.labels_
    iml = newLab.cluster_centers_
    print(iml.shape)
    print(label.shape)
    print("End")
    val = np.zeros((height,width,3))
    index = 0
    for i in range(0, height):
        for j in range(0, width):
            val[i][j][0] = iml[label[index], 0]
            val[i][j][1] = iml[label[index], 1]
            val[i][j][2] = iml[label[index], 2]
            index+=1
    val = lab2rgb(val)
    io.imsave("output/Result" + str(m) + "_MeanShift_B="+str(num)+".jpeg",val)

    return val

def makeKM(im, num):
#KMeans(n_clusters=2).fit(im)
    print("Start")
    newLab = KMeans(n_clusters = num, max_iter=100).fit(im)
    label = newLab.labels_
    iml = newLab.cluster_centers_
    print(iml.shape)
    print(label.shape)
    print("End")
    val = np.zeros((height,width,3))
    index = 0
    for i in range(0, height):
        for j in range(0, width):
            val[i][j][0] = iml[label[index], 0]
            val[i][j][1] = iml[label[index], 1]
            val[i][j][2] = iml[label[index], 2]
            index+=1
    val = lab2rgb(val)
    io.imsave("output/Result" + str(m) + "_K_Means_N="+str(num)+".jpeg",val)

    return val

for root, dirs, files in os.walk('./data'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext in ['.jpg','.png','.gif']:
            new = Image.open('data/'+file)
            lab = rgb2lab(new)
            if(coord == True):
                w = 5
            else:
                w = 3
            im = np.zeros((width*height, w))

            index = 0
            for i in range(0, height):
                for j in range(0, width):
                    im[index, 0] = lab[i][j][0]
                    im[index, 1] = lab[i][j][1]
                    im[index, 2] = lab[i][j][2]
                    if(coord == True):
                        im[index, 3] = j
                        im[index, 4] = i
                    index+=1


            print("Case " + str(m) +": ")

            if(clt == 0):
                #Mean Shift
                st = "MeanShift"
                na = "Bandwidth="
                msimga = makeMShift(im, x)

                msimgb = makeMShift(im,y)

                msimgc = makeMShift(im,z)
            if(clt == 1):
                #K-Means
                st = "K_Means"
                na = "n_clusters="
                msimga = makeKM(im, x)

                msimgb = makeKM(im, y)

                msimgc = makeKM(im, z)

            

 
            if(pic == True):
                

                plt.subplot(221), plt.imshow(new)
                plt.title('Original'), plt.xticks([]), plt.yticks([])

                plt.subplot(222), plt.imshow(msimga)
                plt.title(na + str(x)), plt.xticks([]), plt.yticks([])

                plt.subplot(223), plt.imshow(msimgb)
                plt.title(na + str(y)), plt.xticks([]), plt.yticks([])

                plt.subplot(224), plt.imshow(msimgc)
                plt.title(na + str(z)), plt.xticks([]), plt.yticks([])
            
                plt.savefig('output/Result' + str(m) + '_' + st + '.jpeg')
                plt.clf()


            m += 1
            print("----------------------------------------------")

