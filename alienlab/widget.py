

import matplotlib.pyplot as plt
import ipywidgets as wdg  # Using the ipython notebook widgets
from skimage.transform import resize
from alienlab.utils import clip
import numpy as np

def click_to_graph(mask, im_plot, video_list, time_list, get_fit):
    # Create a random image
    fig, axs = plt.subplots(1, len(video_list)+1, figsize=(5*len(video_list), 4))
    IR = resize(im_plot, mask.shape)

    axs[0].imshow(clip(IR))
    axs[0].axis('off')

    flat_mask = mask.flatten()

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

        for i, video in enumerate(video_list):
            y = np.mean(video[:, pos], axis = 1)    
            x = time_list[i]
            params, ypred = get_fit(y, x, give_y = True)
            axs[i+1].plot(x, ypred, label = params[1])
            axs[i+1].plot(x, y, '.')
            axs[i+1].legend()
 
        
        plt.tight_layout()
    # Create an hard reference to the callback not to be cleared by the garbage collector
    ka = fig.canvas.mpl_connect('button_press_event', onclick)