
from alienlab.improcessing import *
import alienlab.plot
import alienlab.utils

import cv2
import json
import numpy as np
from scipy import ndimage as ndi
import codecs
import io
import PIL

import skimage
import skimage.io
import skimage.morphology
import skimage.filters
import skimage.util 
import skimage.segmentation
import skimage.feature
import skimage.transform
import copy
import matplotlib.pyplot as plt

from tqdm import tqdm

'''MORPHOLOGICAL OPERATIONS BASED ON SKIMAGE'''

def local_maxima(im, min_distance, h, ref_distance = False, mask = None, show = False):
    '''Compute the im local maxima. 
    - im: grey-level image
    - min_distance: minimum number of pixels separating peaks in a 
    region of 2 * min_distance + 1  
    - ref_distance: if True, computes the local maxima of distance map of mask instead of im'''
    # image_max is the dilation of im with a 20*20 structuring element
    # It is used within peak_local_max function
    # Comparison between image_max and im to find the coordinates of local maxima
    local_maxi = skimage.feature.peak_local_max(im, indices = False, min_distance=min_distance)
    
    distance = normalize(ndi.distance_transform_edt(mask))
    dist_local_maxi = skimage.feature.peak_local_max(distance, indices = False, min_distance=min_distance)

    if show == True:
        peaks = np.array([im, im, im])
        maxi = np.asarray([skimage.morphology.binary_dilation(local_maxi), local_maxi*0, local_maxi*0])
        peaks = normalize(peaks + maxi, 0, 1)
        peaks = np.swapaxes(peaks, 0, 1)
        peaks_im = np.swapaxes(peaks, 1, 2)
        peaks = np.array([im, im, im])
        maxi = np.asarray([skimage.morphology.binary_dilation(dist_local_maxi), local_maxi*0, local_maxi*0])
        peaks = normalize(peaks + maxi, 0, 1)
        peaks = np.swapaxes(peaks, 0, 1)
        peaks_dist = np.swapaxes(peaks, 1, 2)
        h.title_list = ['maximum position (im)', 'maximum position (dist)']
        h.save_name = 'local_maxima'
        fig = h.multi([peaks_im, peaks_dist])
        h.saving(fig)
    if ref_distance:
        return dist_local_maxi
    else :
        return local_maxi


def watershed(im, mask, local_maxi, h, ref_distance = False, show = False):
    ''' Segmenting different objects in an image
    - im: image to segment
    - mask: binary mask for the (merged) objects of interest
    - local_maxi: position of the center position of objects of interest
    - ref_distance: if False, uses im for the watershed filling, else uses the distance map of im'''

    # Generate the markers as local maxima of the distance to the background
    markers = ndi.label(local_maxi)[0]
    
    # Distance map of im
    distance = ndi.distance_transform_edt(mask)
    watershed_dist_nomask = skimage.segmentation.watershed(-distance, markers)
    watershed_dist_mask = skimage.segmentation.watershed(-distance, markers, mask=mask)
   
    watershed_im_nomask = skimage.segmentation.watershed(-im, markers)
    watershed_im_mask = skimage.segmentation.watershed(-im, markers, mask=mask)
    
    if show == True:
        h.col_num = 3
        h.title_list = ['Overlapping objects',  'watershed_im','Separated objects',
                        'Distances','watershed_dist', 'Separated_objects' ]
        h.save_name = 'watershed'
        fig = h.multi([im, watershed_im_nomask, watershed_im_mask,
                 -distance, watershed_dist_nomask, watershed_dist_mask])
        h.saving(fig)
    if ref_distance == True: 
        return watershed_dist_mask
    else: 
        return watershed_im_mask
    
def show_segmentation(FRAMES, segmented, h):
    ''' Plot segmentation result (overlap image and segmentation contours '''
    selem = skimage.morphology.disk(1)
    contour = segmented - skimage.morphology.erosion(segmented, selem = selem)
    im_std = grey_to_rgb(normalize(FRAMES.frames_stats['std'], 0, 1))
    im_contour = np.copy(im_std)

    im_contour[:,:,0] = 0
    im_contour[:,:,0] += contour 
    h.figsize = (25, 12)
    h.title_list = ['frames std', 'contours']
    h.save_name = 'result_segmentation'
    fig = h.multi([im_std, im_contour])
    h.saving(fig)

'''LABELME INTERACTION'''


def encodeImageForJson(image):
    #image readable by LabelMe
    img_pil = PIL.Image.fromarray(np.uint8(image), mode='RGB')
    f = io.BytesIO()
    img_pil.save(f, format='PNG')
    data = f.getvalue()
    encData = codecs.encode(data, 'base64').decode()
    encData = encData.replace('\n', '')
    return encData

def segmented_to_json(segmentation, save_path, im_rgb):
    ''' Generates the contour polygons from a segmentation mask with several 
         labels and saves it a json file readable by labelme'''
    
    contours = {}
    for k in np.unique(segmentation):
        if k != 0:
            item = np.uint8(segmentation == k)
            c, hierarchy = cv2.findContours(item, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours[str(k)]=c
    (H, W, d) = im_rgb.shape
    labels_json = {"version": "4.2.10",
                  "flags": {}, 
                  "shapes": [],
                   'imagePath' :  save_path, 
                   'imageData' : encodeImageForJson(im_rgb*255),
                   'lineColor' : alienlab.plot.random_color(255, dim = 4, transparency = 50, div = 1),
                   'fillColor' : alienlab.plot.random_color(255, dim = 4, transparency = 50, div = 1),
                   'imageHeight' : H,
                   'imageWidth' : W,
                  }

    for i, key in enumerate(contours.keys()):
        line_color = alienlab.plot.random_color((255 - i)%255, dim = 4, transparency = 50, div = 1)
        fill_color = line_color.copy()

        shape_dict = {'label' : key, 
                     'line_color': line_color, 
                     'fill_color': fill_color,
                      'points': np.squeeze(contours[key][0], axis = 1).tolist(), 
                      'shape_type': 'polygon',
                      'flags': {}}
        labels_json['shapes'].append(shape_dict)

    with open(alienlab.utils.replace_extension(save_path, '.json'), 'w') as json_file:
        json.dump(labels_json, json_file)
        
def json_to_segmented(json_path, im_basis):
    '''Converts the polygon segmentation contours from a json file to a mask image with several labels '''

    with open(json_path, 'r') as json_file:
        labels_json = json.load(json_file)
    shape_dict = labels_json['shapes']
    im_origin = np.copy(im_basis) * 0
    for shape in shape_dict:
        poly = [np.array(shape['points']).astype(np.int)]
        cv2.fillPoly(im_basis, poly, int(shape['label']))
        cv2.fillPoly(im_origin, poly, int(shape['label']))
        cv2.putText(im_basis, "{}".format(shape['label']), (int(shape['points'][0][0]) - 10, int(shape['points'][0][1])),
		cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
    return im_basis, im_origin



def uniform_mask(im, N, plot = False):
    """Create a mask whith discrete values associated to a grid of image im with size N"""
    L,H,_ = im.shape
    mask = copy.copy(im[:,:,0])*0
    d = 0
    for i in range(L//N):
        for j in range(H//N):
            mask[i*N:(i+1)*N,j*N:(j+1)*N] = d
            d+=1
    if plot == True:
        plt.figure(figsize = (3,3))
        plt.imshow(mask)

    return mask, (L,H), (L//N, H//N)



def label_to_data(mask, FO):
    # Item time trajectories with overlaps
    # create a dictionnary with one entry for each item:
    '''
    { '1.0': {'x_coords': np array, x coordinates in HQ}
                'y_coords': np array,  y coordinates in HQ
                'binned_coords': set, couples of (x,y) coordinates in binned video
                'surface': number of pixels in the item in HQ
                'pixel_values': array, size: (N, s) where N is number of frames and s surface
                'mean': array, size N, mean value of the item intensity for each frame
                'std':  array, size N, std value of the item intensity for each frame
                'remains' : True, the item is present in this segmentation step
                }
    '2.0': {'x_coords'...
                    }
        }
    '''
    segmented = mask
    items = np.unique(segmented) #returns the set of values in items, corresponds to the values of the markers of local_maxima

    items_dict = {}
    for k in tqdm(items):
        x_coords, y_coords = np.nonzero(segmented == k)
        pixel_values = FO.frames[:,x_coords, y_coords]

        key = str(k)
        items_dict[key] = {}
        items_dict[key]['x_coords'] = x_coords
        items_dict[key]['y_coords'] = y_coords
        items_dict[key]['pixel_values'] = pixel_values
        items_dict[key]['surface'] = pixel_values.shape[1]
        items_dict[key]['mean'] = np.mean(pixel_values, axis = 1)
        items_dict[key]['std'] = np.std(pixel_values, axis = 1)
        items_dict[key]['remains'] = True

    return items_dict