import os
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA

pnum = 2000
facenum = 320
people = 10
facerecog = 20
testcase = 5*people + facerecog
list = []

def nextmax(list, max):
    value = float('-inf')
    for i in range(0, facenum):
        if(list[i] > value and list[i] < max):
            value = list[i]
    return value

def nextmin(list, min):
    value = float('inf')
    for i in range(0, facenum):
        if(list[i] < value and list[i] > min):
            value = list[i]
    return value

for root, dirs, files in os.walk('./data'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext in ['.jpg','.png','.gif']:
            im = Image.open('data/'+file)
            for i in range(0,32):
                for j in range(0,32):
                    list.append(im.getpixel((j,i)))


mat = np.matrix(list)
mat = np.transpose(np.reshape(mat, (pnum,1024)))
mean = np.mean(mat, axis=1)
for i in range(0,pnum):
    mat[:,i] = mat[:,i]-mean

meanface = np.reshape(mean, (32,32))
mim = Image.fromarray(meanface)
mim = mim.convert('L')
mim.save('mean.jpg')

pca = PCA(n_components = facenum)
V = pca.fit_transform(mat)

#V = 1024 by facenum matrice

eigenlist = []
for i in range(0, facenum):
    eigenface = np.reshape(V[:,i], (1024,1))
    eigenlist.append(eigenface)
    eigenface = np.reshape(eigenface+128, (32,32))
    fim = Image.fromarray(eigenface)
    fim = fim.convert('L')
    fim.save('eigenface/eigenface' + str(i) + '.jpg')


newlist = []
coeff = []
allcoeff = []

start = 1

for root, dirs, files in os.walk('./test'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext in ['.jpg','.png','.gif']:
            im = Image.open('test/'+file)
            newlist.clear()
            coeff.clear()
            testindex = 1
            for i in range(0,32):
                for j in range(0,32):
                    newlist.append(im.getpixel((j,i)))

            newmat = np.matrix(newlist)
            newmat = newmat - np.transpose(mean)
            
            for i in range (0, facenum):
                coeff.append((newmat @ eigenlist[i])/np.dot(np.transpose(eigenlist[i]), eigenlist[i]))
           # print(coeff)
            sum = 0
            for i in range (0, facenum):
                sum = sum + (float(coeff[i]) * eigenlist[i])
                
                if(testindex == 2 or testindex == 3 or testindex == 5 or testindex == 10 or testindex%20 == 0 or testindex == facenum):
                    picture = np.reshape(sum+mean, (32,32))
                    pim = Image.fromarray(picture)
                    pim = pim.convert('L')
                    pim.save('output/' + str(start) + "-" + str(testindex) + '.jpg')

                testindex = testindex+1
            start = start+1
            for i in range(0, facenum):
                allcoeff.append(coeff[i])

##################################
####     FACE RECOGNITION     ####
##################################

            
lookd = 7
lookup = [89,135,206,65,43,231,79, 82,303,70,91,128,178,58, 27,295,56,181,274,210,205, 168,203,108,124,218,122,242, 165,92,195,192,71,241,148, 239,46,155,87,234,94,315, 262,69,93,185,64,307,292, 0,81,261,130,186,310,223, 24,191,264,294,164,271,290, 248,154,95,14,42,225,222]
name = ["Ryu", "Chim", "IU", "Pheonix", "Dakota", "LeeBH", "Zoe", "LeBron", "Anna", "Jason"]

newnew = []

for i in range(0, facerecog):
    newnew.clear()
    for j in range(0, people):
        meann = 0
        for k in range(0,lookd): #lookup index
            cha = 0
            for w in range(0,5): #people picture
                cha += abs(allcoeff[facenum*(50 + i) + lookup[lookd*j + k]] - allcoeff[facenum*(j*5+w) + lookup[lookd*j + k]])
            meann = meann+cha/5
        meann = meann/lookd
        newnew.append(meann)
    print("Recog "+ str(i+1) + ": " + name[newnew.index(np.min(newnew))])


##################################
####        END OF CODE       ####
##################################
####           WA!!!          ####
####          SANS!!!         ####
##################################
#██████████▀▀▀▀▀▀▀▀▀▀▀▀▀██████████
#█████▀▀░░░░░░░░░░░░░░░░░░░▀▀█████
#███▀░░░░░░░░░░░░░░░░░░░░░░░░░▀███
#██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██
#█░░░░░░▄▄▄▄▄▄░░░░░░░░▄▄▄▄▄▄░░░░░█
#█░░░▄██▀░░░▀██░░░░░░██▀░░░▀██▄░░█
#█░░░██▄░░▀░░▄█░░░░░░█▄░░▀░░▄██░░█
#██░░░▀▀█▄▄▄██░░░██░░░██▄▄▄█▀▀░░██
#███░░░░░░▄▄▀░░░████░░░▀▄▄░░░░░███
#██░░░░░█▄░░░░░░▀▀▀▀░░░░░░░█▄░░░██
#██░░░▀▀█░█▀▄▄▄▄▄▄▄▄▄▄▄▄▄▀██▀▀░░██
#███░░░░░▀█▄░░█░░█░░░█░░█▄▀░░░░███
#████▄░░░░░░▀▀█▄▄█▄▄▄█▄▀▀░░░░▄████
#███████▄▄▄▄░░░░░░░░░░░░▄▄▄███████
"""
printnum = 50
var = []
for k in range(0,people):
    print("--------------------" + str(k+1) + " Case :" + "--------------------")
    for i in range(0,printnum):
        print(str(i) + ":")
        var.clear()
        for j in range(0,5):
            var.append(allcoeff[facenum*5*k + facenum*j + i])
            print(np.std(var))


for w in range(0, facerecog):
    print("Picture " + str(w+1) + ":")
    for i in range(0, people):   # People at what number?
        dis = 0
        for k in range(0, facenum):    #What coefficeint?
            m = 0
            for j in range(0, 5):    #Collecting same person's pictures
                m = m + allcoeff[5*i*facenum + j*facenum + k]    
            m = m/5
            dis = dis + (m-allcoeff[(testcase-facerecog)*facenum + w*facenum + k])**2
        a = np.sqrt(dis)
        print("Case " + str(i+1) + ": " + str(a))
    print("------------------------------")


    dis = []
    for w in range(0, facerecog):
    print("Picture " + str(w+1) + ":")
    for i in range(0, people):   # People at what number?
        dis.clear()
        for j in range(0, 5):    #Collecting same person's pictures
            s = 0
            for k in range(0, facenum):    #What coefficeint?
                s = s + (allcoeff[5*i*facenum + j*facenum + k]-allcoeff[(testcase-facerecog)*facenum + w*facenum + k])**2
            dis.append(np.sqrt(s))
        a = np.min(dis)
        print("Case " + str(i+1) + ": " + str(a))
    print("------------------------------")



@@@@@@@@ 5. Finding Largest Coefficient @@@@
    for i in range(0, people):   # People at what number?
    print("Case "+ str(i) + "\n--------------------------")
    for j in range(0, 5):    #Collecting same person's pictures
        max = 10000
        for u in range(0, 160):
            max = nextmax(allcoeff[facenum*i*5  + facenum*j : facenum*i*5  + facenum*(j+1)], max)
            index = allcoeff.index(max) - (facenum*i*5  + facenum*j)
            print(str(u) + ": MAX at: " + str(index) + "  value:" + str(max))
    print("\n---------------------------------------")


@@@@@@@@@@ Chai Jagun Coeff Chazaboza
    dis = []
    for i in range(0, people):   # People at what number?
    dis.clear()
    print("Case "+ str(i) + "\n----------------------------------")
    for k in range(0, facenum):
        m = 0
        for j in range(0, 4):    #Collecting same person's pictures allcoeff[facenum*i*5  + facenum*j : facenum*i*5  + facenum*(j+1)]
            for a in range(j+1, 5):
                cha = abs(allcoeff[facenum*i*5  + facenum*j + k] - allcoeff[facenum*i*5  + facenum*a + k])
                m += cha
        m = m/10
        dis.append(m)
    min = -1000000
    for u in range(0, 10):
        min = nextmin(dis, min)
        index = dis.index(min)
        print(str(u) + ": Min at: " + str(index) + " val: " + str(min))
    print("\n----------------------------------")
"""
# Gwalmok SSap Possible
"""
dis = []
m = []
for i in range(0, people):   # People at what number?
    dis.clear()
    print("Case "+ str(i) + "\n----------------------------------")
    for k in range(0, facenum): #What coeff?
        m.clear()
        for j in range(0, 5):    #Collecting same person's pictures allcoeff[facenum*i*5  + facenum*j : facenum*i*5  + facenum*(j+1)]
            m.append(allcoeff[facenum*(i*5 + j) + k])
        dis.append(abs(np.mean(m)) / np.var(m))
    max = float('inf')
    for u in range(0, 40):
        max = nextmax(dis, max)
        index = dis.index(max)
        print(str(u) + ": " + str(index))
    print("\n---------------------------------------")
"""

