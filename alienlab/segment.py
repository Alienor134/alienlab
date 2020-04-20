
from alienlab.improcessing import *
import alienlab.plot

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
        maxi = np.asarray([skimage.morphology.binary_dilation(local_maxi), local_maxi*0, local_maxi*0])
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
    
    if show == False:
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
        line_color = alienlab.plot.random_color(255 - i, dim = 4, transparency = 50, div = 1)
        fill_color = line_color.copy()

        shape_dict = {'label' : key, 
                     'line_color': line_color, 
                     'fill_color': fill_color,
                      'points': np.squeeze(contours[key][0], axis = 1).tolist(), 
                      'shape_type': 'polygon',
                      'flags': {}}
        labels_json['shapes'].append(shape_dict)

    with open(alienlab.io.replace_extension(save_path, '.json'), 'w') as json_file:
        json.dump(labels_json, json_file)
        
def json_to_segmented(json_path):
    '''Converts the polygon segmentation contours from a json file to a mask image with several labels '''

    with open(json_path, 'r') as json_file:
        labels_json = json.load(json_file)
    shape_dict = labels_json['shapes']
    im_segmented = np.zeros((labels_json['imageHeight'], labels_json['imageWidth']))
    for shape in shape_dict:
        poly = [np.array(shape['points']).astype(np.int)]
        cv2.fillPoly(im_segmented, poly, int(shape['label']))
    return im_segmented