import os
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA

pnum = 1600
facenum = 64
testcase = 10
list = []

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

U, s, V = np.linalg.svd(mat)

#eigval, eigvec = np.linalg.eig(mat@np.transpose(mat))
#eigvec: 1024 * 1024

#pca = PCA(n_components = facenum)
#V = pca.fit_transform(mat)

#V = 1024 by facenum matrice

#index = []
#for i in range(0,1024):
#    t = (i, s[i])
#    index.append(t)
#    
#index.sort(key = lambda element : element[1], reverse=True)

eigenlist = []
for i in range(0, facenum):
    eigenface = np.reshape(V[:1024,i], (1024,1))*1024
    eigenlist.append(eigenface)
    eigenface = np.reshape(eigenface + mean, (32,32))
    fim = Image.fromarray(eigenface)
    fim = fim.convert('L')
    fim.save('eigenface' + str(i) + '.jpg')

 
newlist = []
coeff = []
testindex = 1
for root, dirs, files in os.walk('./test'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext in ['.jpg','.png','.gif']:
            im = Image.open('test/'+file)
            newlist.clear()
            coeff.clear()
            for i in range(0,32):
                for j in range(0,32):
                    newlist.append(im.getpixel((j,i)))

            newmat = np.matrix(newlist)
            newmat = newmat - np.transpose(mean)
            
            for i in range (0, facenum):
                coeff.append(newmat @ eigenlist[i])

            sum = 0
            for i in range (0, facenum):
                sum = sum + (float(coeff[i]) * eigenlist[i])
                               
            print("Case " + str(testindex) + ":\n")
            print(np.mean(coeff))
            print("--------------------------------------------------------------")

            picture = np.reshape(sum+mean, (32,32))
            pim = Image.fromarray(picture)
            pim = pim.convert('L')
            pim.save('output' + str(testindex) + '.jpg')
            testindex = testindex+1
           