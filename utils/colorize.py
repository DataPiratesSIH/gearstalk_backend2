import time
import binascii
import struct
from PIL import Image
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import cv2
import matplotlib.colors as mc
from utils.colorlist import colours

NUM_CLUSTERS = 3
mycss4list = mc.CSS4_COLORS.items()

def nearest_colour( subjects, query ):
    return min( subjects, key = lambda subject: sum( (s - q) ** 2 for s, q in zip( subject, query ) ) )

def colorize(image):
    
    ''' 
    the input image is in opencv format.
    Convert it to PIL format
    '''
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)                                # convert the color.
    im = Image.fromarray(img)


    # im = Image.open('./woman.jpg')
    im = im.resize((100, 100))                                                  # optional, to reduce time
    ar = np.asarray(im)
    shape = ar.shape
    ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)


    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)                     #finding clusters of similar colors

    vecs, dist = scipy.cluster.vq.vq(ar, codes)                                 # assign codes
    counts, bins = np.histogram(vecs, len(codes))                               # count occurrences

    index_max = np.argsort(counts)[::-1]                                        # find most frequent

    '''
     peak = codes[index_max]
     codes = codes.astype('int32')
     colors =[list(codes[index_max[0]]),list(codes[index_max[1]])]
     '''
    
    color1 = nearest_colour( colours, tuple(codes[index_max[0]]) )[3]
    color2 = nearest_colour( colours, tuple(codes[index_max[1]]) )[3]

    '''colors in hexadecimal format

     colour1 = '#' + binascii.hexlify(bytearray(int(c) for c in codes[index_max[0]])).decode('ascii')
     print('most frequent is %s (#%s)' % (codes[index_max[0]], colour1))
     colour2 = '#' + binascii.hexlify(bytearray(int(c) for c in codes[index_max[1]])).decode('ascii')
     print('most frequent is %s (#%s)' % (codes[index_max[1]], colour2))
    
    '''
    colors = [color1,color2]

    return colors