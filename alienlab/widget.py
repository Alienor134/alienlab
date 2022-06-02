

import matplotlib.pyplot as plt
import ipywidgets as wdg  # Using the ipython notebook widgets
from skimage.transform import resize
from alienlab.utils import clip
import numpy as np
from IPython.display import display



def click_to_1_graph(mask, im_plot, video, time):
    fig, axs = plt.subplots(1, 2 , figsize=(15, 8))
    IR = resize(im_plot, mask.shape)
    flat_mask = mask.flatten()
    video = video.reshape(video.shape[0], -1)
    axs[0].imshow(IR)
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
                y = np.mean(video[:, pos], axis = 1)    
                x = time
                axs[1].plot(x, y, '-')
    
            
        plt.tight_layout()
    # Create an hard reference to the callback not to be cleared by the garbage collector
    ka = fig.canvas.mpl_connect('button_press_event', onclick)    

##############
def click_to_graph(mask, im_plot, video_list_init, time_list, get_fit, clipit = True, col = 3, figsize=(0,0)):
    # Create a random image
    L = len(video_list_init)+1
    
    if figsize == (0,0):
        fig, axs = plt.subplots(col, L//col + 1 , figsize=(5*(L//col), 10))
    else:
        fig, axs = plt.subplots(col, L//col + 1, figsize=figsize)
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
                axs[(i+1)%col][(i+1)//col].plot(x, ypred, label = params[1])
                axs[(i+1)%col][(i+1)//col].plot(x, y, '-')
                axs[(i+1)%col][(i+1)//col].legend()
    
            
        plt.tight_layout()
    # Create an hard reference to the callback not to be cleared by the garbage collector
    ka = fig.canvas.mpl_connect('button_press_event', onclick)