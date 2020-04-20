import numpy as np
import skimage.filters
import skimage.util



def make_binary(im, radius = 15, soft_hard = 1, threshold = None, show = False):
    '''Converts grey-level image to binary image using Otsu local threshold'''
    # otsu threshold locally
    # soft_hard parameters adds a weight on the threshold. >1 favors false negatives, <1 favors false_positives
    # threshold allows to manually force the threshold
    if threshold == None:
        img = skimage.util.img_as_ubyte(im/im.max())
        threshold_global_otsu = skimage.filters.threshold_otsu(img)
        global_otsu = img >= threshold_global_otsu * soft_hard
    
    else:
        global_otsu = im >= threshold
        
    return global_otsu

def grey_to_rgb(im):
    '''1D image to 3D image'''
    return np.repeat(im[:,:,np.newaxis],3,axis = 2)

def normalize(im, min_target = 0, max_target = 1):
    ''' Normalise image within range [min_target, max_target]'''
    min_val = im.min()
    max_val = im.max()
    im = (im - min_val) * max_target/(max_val - min_val) + min_target
    return im
