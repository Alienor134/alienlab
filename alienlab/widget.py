

import matplotlib.pyplot as plt
import ipywidgets as wdg  # Using the ipython notebook widgets
from skimage.transform import resize
from alienlab.utils import clip
import numpy as np

def click_to_graph(mask, im_plot, video_list_init, time_list, get_fit, clipit = True, figsize=(0,0)):
    # Create a random image
    L = len(video_list_init)+1
    col  = 4
    if figsize == (0,0):
        fig, axs = plt.subplots(L//col, col , figsize=(15, 5*(L//3)))
    else:
        fig, axs = plt.subplots(L//col, col, figsize=figsize)
    IR = resize(im_plot, mask.shape)
    if clipit == True:
        axs[0][0].imshow(clip(IR))
    else: 
        axs[0][0].imshow(IR)
    axs[0][0].axis('off')

    flat_mask = mask.flatten()

    video_list = []
    for video in video_list_init:
        if video.shape[0]!=0:
            video_list.append(video)

    for i, video in enumerate(video_list): 
        video_list[i] = video.reshape(video.shape[0], -1)

    # Create and display textarea widget
    txt = wdg.Textarea(
        value='',
        placeholder='',
        description='event:',
        disabled=False
    )
    display(txt)


    # Define a callback function that will update the textarea
    def onclick(event):
        global ix, iy
        ix, iy = event.xdata, event.ydata
        txt.value = str(event)#"x= %d, y = %d"%(ix, iy)

        ind = mask[iy.astype(int), ix.astype(int)]
        pos = flat_mask == ind
        if ind != 0:
            for i, video in enumerate(video_list):
                y = np.mean(video[:, pos], axis = 1)    
                x = time_list[i]
                params, ypred = get_fit(y, x, give_y = True)
                axs[(i+1)//col][(i+1)%col].plot(x, ypred, label = params[1])
                axs[(i+1)//col][(i+1)%col].plot(x, y, '.')
                axs[(i+1)//col][(i+1)%col].legend()
    
            
        plt.tight_layout()
    # Create an hard reference to the callback not to be cleared by the garbage collector
    ka = fig.canvas.mpl_connect('button_press_event', onclick)