import os
from PIL import Image
import numpy as np
from sklearn.decomposition import PCA
from scipy.fftpack import dct, idct

rmat = np.zeros(shape = (720,1280))
gmat = np.zeros(shape = (720,1280))
bmat = np.zeros(shape = (720,1280))
blocksize = 16
q_size = 64

def nextmax(mat, max):
    value = float('-inf')
    for i in range(0, blocksize):
        for j in range(0,blocksize):
            if(abs(mat[i,j]) >= abs(value) and abs(mat[i,j]) <= abs(max)):
                value = mat[i,j]
    return value

def dct2 (block):
    return dct(dct(block.T, norm = 'ortho').T, norm = 'ortho')

def idct2 (block):
    return idct(idct(block.T, norm = 'ortho').T, norm = 'ortho')

def select(mat):
    max = float('inf')
    for u in range(0, np.size(mat)):
        max = nextmax(mat, max)
        if(u>=blocksize):
            mat[np.where(mat == max)] = 0
    return mat

def select2(mat):
    t = abs(np.ravel(mat, order = 'C')).argsort()
    q = np.zeros(mat.shape, 'int')

    for x in range(0, q_size):
        m = int(x/16)
        n = x%16
        q[m,n] = mat[m,n]

    return q

def det(x):
    if(x<0):
        return 0
    if(x>255):
        return 255
    else:
        return x

index = 0
for root, dirs, files in os.walk('./data'):
    for idx, file in enumerate(files):
        fname, ext = os.path.splitext(file)
        if ext in ['.jpg','.png','.gif', '.bmp']:
            im = Image.open('data/'+file)
            im = im.convert('RGB')
            im.save('output/new' + str(index) + '.bmp')
            for j in range(0,1280):
                for i in range(0,720):
                   rmat[i,j] = im.getpixel((j,i))[0]
                   gmat[i,j] = im.getpixel((j,i))[1]
                   bmat[i,j] = im.getpixel((j,i))[2]

            # Pictures that will be saved

            rnew = np.zeros(shape = (720,1280))
            gnew = np.zeros(shape = (720,1280))
            bnew = np.zeros(shape = (720,1280))

            # DCT start

            rblock = np.zeros(shape = (blocksize, blocksize))
            gblock = np.zeros(shape = (blocksize, blocksize))
            bblock = np.zeros(shape = (blocksize, blocksize))
            for i in range(0, int(720/blocksize)):
                for j in range(0, int(1280/blocksize)):
                    for a in range(0,blocksize):
                        for b in range(0,blocksize):
                            rblock[a,b] = rmat[blocksize*i+a, blocksize*j+b]
                            gblock[a,b] = gmat[blocksize*i+a, blocksize*j+b]
                            bblock[a,b] = bmat[blocksize*i+a, blocksize*j+b]

                    rblock = dct2(rblock)
                    gblock = dct2(gblock)
                    bblock = dct2(bblock)
                
                    irblock = idct2(select2(rblock))
                    igblock = idct2(select2(gblock))
                    ibblock = idct2(select2(bblock))

                    for a in range(0,blocksize):
                        for b in range(0,blocksize):

                            rnew[blocksize*i+a, blocksize*j+b] = det(irblock[a,b])
                            gnew[blocksize*i+a, blocksize*j+b] = det(igblock[a,b])
                            bnew[blocksize*i+a, blocksize*j+b] = det(ibblock[a,b])
            # Save img

            rgbArray = np.zeros((720, 1280,3), 'uint8')
            rgbArray[:,:,0] = rnew
            rgbArray[:,:,1] = gnew
            rgbArray[:,:,2] = bnew
        
            #print(rgbArray)

            pim = Image.fromarray(rgbArray)
            pim = pim.convert('RGB')
            pim.save('output/output '+ str(q_size) + '-' + str(index) + '.bmp')
            index += 1

print("End of Code")