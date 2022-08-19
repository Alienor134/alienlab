import os
import sys
import numpy as np
import random
import pandas as pd
import copy
from tkinter.filedialog import askdirectory, askopenfilename
import matplotlib.pyplot as plt
from collections import OrderedDict

marker = [".", "s","o","v","^","<",">","1","2","3","4","8","p","P","*","h","H","+","x","X","D","d","|","_",0,1,2,3,4,5,6,7,8,9,10,11
]

hatch = [ "////" , "\\\\" , "||||" , "----" , "...." , "xxxx", "oooo", "O"]

linestyles = OrderedDict(
    [('solid',               (0, ())),
     ('loosely dotted',      (0, (1, 10))),
     ('dotted',              (0, (1, 5))),
     ('densely dotted',      (0, (1, 1))),

     ('loosely dashed',      (0, (5, 10))),
     ('dashed',              (0, (5, 5))),
     ('densely dashed',      (0, (5, 1))),

     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])


linestyle =  ['--', '-.', '-', ':', '', ' ']

color = plt.get_cmap('jet')(np.linspace(0, 1, 20))

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

def pandas_to_arrays(file, skiprows=None, skipfooter=0):
    df = pd.read_csv(file, skiprows=skiprows, skipfooter=skipfooter)

    headers = np.array(df.keys())
    data = []
    for head in headers:
        y = np.array(df[head])
        y = y[y==y]
        data.append(y)
        
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