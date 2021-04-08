import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
from random import *
from sklearn.preprocessing import MinMaxScaler
import scipy.stats as stats
from skimage.color import rgb2yuv

image = 10
scaler = MinMaxScaler((0,255))

pic = True

R = []
G = []
B = []
Y = []
U = []
V = []

width = 640
height = 360

m=1

def makeimg(array):
    nim = Image.fromarray(array)
    
    return nim

for root, dirs, files in os.walk('./data'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext in ['.jpg','.png','.gif']:
            im = Image.open('data/'+file)

            pix = np.array(im)
            yuv = rgb2yuv(im)
            
            R.clear()
            G.clear()
            B.clear()
            Y.clear()
            U.clear()
            V.clear()

            print("Case " + str(m) +": ")
            
            for i in range(0, height):
                for j in range(0, width):
                    R.append(pix[i][j][0])
                    G.append(pix[i][j][1])
                    B.append(pix[i][j][2])
                    Y.append(yuv[i][j][0])
                    U.append(yuv[i][j][1])
                    V.append(yuv[i][j][2])
              
            GRcorr = stats.pearsonr(G, R)
            RBcorr = stats.pearsonr(R, B)
            GBcorr = stats.pearsonr(B, G)
            YUcorr = stats.pearsonr(Y, U)
            YVcorr = stats.pearsonr(Y, V)
            UVcorr = stats.pearsonr(U, V)

            print("G-R Corrleation: " + str(GRcorr))
            print("G-B Corrleation: " + str(GBcorr))
            print("R-B Corrleation: " + str(RBcorr))
            print("Y-U Corrleation: " + str(YUcorr))
            print("Y-V Corrleation: " + str(YVcorr))
            print("U-V Corrleation: " + str(UVcorr))   
 
            if(pic == True):
                Rpix = np.array(im)
                Rpix[:,:,1] = 0
                Rpix[:,:,2] = 0
                Rim = makeimg(Rpix)

                Gpix = np.array(im)
                Gpix[:,:,0] = 0
                Gpix[:,:,2] = 0
                Gim = makeimg(Gpix)
                
                Bpix = np.array(im)
                Bpix[:,:,1] = 0
                Bpix[:,:,0] = 0
                Bim = makeimg(Bpix)

                plt.subplot(221), plt.imshow(im)
                plt.title('Original'), plt.xticks([]), plt.yticks([])

                plt.subplot(222), plt.imshow(Rim)
                plt.title('R'), plt.xticks([]), plt.yticks([])

                plt.subplot(223), plt.imshow(Gim)
                plt.title('G'), plt.xticks([]), plt.yticks([])

                plt.subplot(224), plt.imshow(Bim)
                plt.title('B'), plt.xticks([]), plt.yticks([])
            
                plt.savefig('output/RGB' + str(m) + '.jpeg')
                plt.clf()


            m += 1
            print("----------------------------------------------")

