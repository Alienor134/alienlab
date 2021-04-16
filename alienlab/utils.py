import os
import sys
import numpy as np
import random
import pandas as pd

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


def pandas_to_arrays(file):
    df = pd.read_csv(file)

    headers = np.array(df.keys())
    data = []
    for head in headers:
        data.append(np.array(df[head]))
        
    return headers, data
        
    