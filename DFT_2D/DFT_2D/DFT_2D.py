import numpy as np
import os
from PIL import Image
import matplotlib.pyplot as plt
from random import *
from sklearn.preprocessing import MinMaxScaler

pixel = 64
numberAx = 25
numberBx = 85
numberAy = 100
numberBy = 75
image = 20
scaler = MinMaxScaler()

pic = False

normal = []
m = 1

for root, dirs, files in os.walk('./data'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext in ['.jpg','.png','.gif']:
            im = Image.open('data/'+file)
          
            sampleA = im.crop((numberAx, numberAy, numberAx + pixel, numberAy + pixel))
            sampleB = im.crop((numberBx, numberAy, numberBx + pixel, numberAy + pixel))
            sampleC = im.crop((numberAx, numberBy, numberAx + pixel, numberBy + pixel))
            sampleD = im.crop((numberBx, numberBy, numberBx + pixel, numberBy + pixel))

            dftA = np.fft.fft2(sampleA.convert('L'))
            dftB = np.fft.fft2(sampleB.convert('L'))
            dftC = np.fft.fft2(sampleC.convert('L'))
            dftD = np.fft.fft2(sampleD.convert('L'))
            
            sdftA = np.fft.fftshift(dftA)
            sdftB = np.fft.fftshift(dftB)
            sdftC = np.fft.fftshift(dftC)
            sdftD = np.fft.fftshift(dftD)
            
            magnitudeA = 20*np.log(np.abs(sdftA))
            magnitudeB = 20*np.log(np.abs(sdftB))
            magnitudeC = 20*np.log(np.abs(sdftC))
            magnitudeD = 20*np.log(np.abs(sdftD))

            normal.append(scaler.fit_transform(magnitudeA))
            normal.append(scaler.fit_transform(magnitudeB))
            normal.append(scaler.fit_transform(magnitudeC))
            normal.append(scaler.fit_transform(magnitudeD))
            
            if(pic == True):
                plt.subplot(241), plt.imshow(sampleA)
                plt.title('sample A'), plt.xticks([]), plt.yticks([])

                plt.subplot(242), plt.imshow(magnitudeA, cmap='gray')
                plt.title('magnitude A'), plt.xticks([]), plt.yticks([])

                plt.subplot(243), plt.imshow(sampleB)
                plt.title('sample B'), plt.xticks([]), plt.yticks([])

                plt.subplot(244), plt.imshow(magnitudeB, cmap='gray')
                plt.title('magnitude B'), plt.xticks([]), plt.yticks([])

                plt.subplot(245), plt.imshow(sampleC)
                plt.title('sample C'), plt.xticks([]), plt.yticks([])

                plt.subplot(246), plt.imshow(magnitudeC, cmap='gray')
                plt.title('magnitude C'), plt.xticks([]), plt.yticks([])

                plt.subplot(247), plt.imshow(sampleD)
                plt.title('sample D'), plt.xticks([]), plt.yticks([])

                plt.subplot(248), plt.imshow(magnitudeD, cmap='gray')
                plt.title('magnitude D'), plt.xticks([]), plt.yticks([])
            
                plt.savefig('output/magnitude' + str(m) + '.jpeg')
                plt.clf()

ans = 0
mark = 0
dist = []
for root, dirs, files in os.walk('./data'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext in ['.jpg','.png','.gif']:
            im = Image.open('data/'+file)
            
            for i in range(0,5):
                dist.clear()
                sx = randint(0,160)
                sy = randint(0,160)

                try:
                    testcase = im.crop((sx, sy, sx + pixel, sy + pixel))
                    dfttest = np.fft.fft2(testcase.convert('L'))
                    sdfttest = np.fft.fftshift(dfttest)
                    magnitest = 20*np.log(np.abs(sdfttest))
                    magnitest = scaler.fit_transform(magnitest)
                except ValueError:
                    i = i-1
                    pass
                for j in range(0,image):
                    mean = 0
                    for k in range(0,4):
                        mean += np.linalg.norm(magnitest - normal[j*4 + k])
                    dist.append(mean/4)

                fore = dist.index(min(dist))
                
                if(fore == ans):
                    print("Correct! Expected " + str(ans+1) + " Returned " + str(fore+1))
                    mark += 1
                else:
                    print("Wrong... Expected " + str(ans+1) + " Returned " + str(fore+1))
            ans += 1


print("------------------------------------")
print("Correctness: " + str(mark) + "%")
if(mark == 100):
    print("100% Correct!!! Congraturations!!!")
if(mark >= 95 and mark != 100):
    print("Very High Correctness!! Well Done!!")
if(mark >= 90 and mark <95):
    print("High Correctness! Nice!")
                
