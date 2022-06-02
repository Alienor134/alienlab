import os
import sys
import numpy as np
import random
import pandas as pd
import copy
from tkinter.filedialog import askdirectory, askopenfilename


def set_filename():
    file = askopenfilename()
    return file

def set_directory():
    direc = askdirectory()
    return direc

def create_folder_if(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def replace_extension(file_path, new_ext):
    new_path = os.path.splitext(file_path)[0] + new_ext
    return new_path

def random_color(num, dim = 3, transparency = 128, div = 255):
    if num < 1:
        num = (num * 255)//1
    num = int(num)
    R = random.randint(0, num)
    G = random.randint(0, num - R)
    B = random.randint(0, num - R - G)
    color = [R/div, G/div, B/div]
    random.shuffle(color)
    if dim == 1:
        return color[0]
    if dim == 4:
        return color + [transparency]
    else: 
        return color


def clip(input_image, high = 90, low = 10):
    im = copy.copy(input_image)
    im[im<np.percentile(im, low)]=np.percentile(im, low)
    im[im>np.percentile(im, high)]=np.percentile(im, high)
    return im

def pandas_to_arrays(file):
    df = pd.read_csv(file)

    headers = np.array(df.keys())
    data = []
    for head in headers:
        data.append(np.array(df[head]))
        
    return headers, data
        
def tiff_to_video():
    from tkinter.filedialog import askopenfilename
    import numpy as np
    import cv2
    import imageio
    filename = askopenfilename()
    vid_name = os.path.split(filename)[0] + "/video_converted.mp4"
    print(vid_name)
    
    out = cv2.VideoWriter(vid_name, cv2.VideoWriter_fourcc(*'mp4v'), 6, (968, 608), False)

        
    reader = imageio.get_reader(filename)
    for im in reader:
            video_frame = np.array(im)
            video_frame = video_frame*255.0/(np.max(video_frame))
            video_frame =video_frame.astype(dtype='uint8')
            out.write(video_frame)
    out.release()