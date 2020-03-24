# -*- coding: utf-8 -*-


"""
Created on Thu Feb 14 22:29:53 2019

@author: Alienor Lahlou
"""


"""OPEN FILE"""

import os
import sys
cwd = os.getcwd()
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import datetime


def create_folder_if(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def catch_file(direc = cwd ):
    """Opens a dialog window to select a file. Default directory: current directory
    direc [str]: directory to open (default: current directory)
    """
    
    from PyQt5 import QtWidgets, QtGui
    app = QtWidgets.QApplication(sys.argv)
    fname = QtWidgets.QFileDialog.getOpenFileName(None, directory=direc, caption = "Select a video file...",
                                                  filter="All files (*)")
    return fname[0]

"""PLOTS"""

class plotclass(object):
    """This class contains functions that can plot graphs and several curves on a graph (and save the plot)
    Input: x [array or list/tuple of arrays]: x axis values, either one array or multiple arrays
    Input: y [array or list/tuple of arrays]: x axis values, either one array or multiple arrays
    Output: plot f(x) = y, or overlayed curves f(xi) = yi"""
        
    def __init__(self, xval=None, yval=None):
        #plot parameters
        self.figsize = (9, 6)
        self.fontsize = 13
        self.color = 'steelblue'
        self.marker = 'o-'
        self.linewidth = 2
        self.title = 'My Title'
        
        #saving parameters
        self.date = True
        self.save_name = 'Figure'
        self.extension = '.tiff'
        
        #multiplot parameters
        self.label_item = ['MyLabel']
        self.label_list = self.label_item * 100
        self.color_list = [self.color] + ['indianred', 'seagreen', 'mediumslateblue', 'maroon', 'palevioletred'
                          'orange', 'lightseagreen', 'dimgrey', 'slateblue']


        self.xval = xval
        self.yval = yval
        
        #axis formatting
        self.xlabel = 'x label (unit)'
        self.ylabel = 'y label (unit)'
        self.sample = 10
        self.subsample = 5
        self.ylog = ''
        
        #coplotting
        self.y2val = []
        self.x2val = []
        self.label2_list = []
        self.y2label = 'y2 label (unit)'
        self.y2log = ''

    
    def pretreat(self, X, Y):
        if type(X) != tuple and type(X) != list: #converts to a list if there is only one element
            X = [X]
        
        if type(Y) != tuple and type(Y) != list: #converts to a list if there is only one element
            Y = [Y]
            
        NX = len(X)
        NY = len(Y)
        if NX != NY:
            if NX != 1:
                print('OooOouups! X should be a list or tuple containing either 1 array or the same number of arrays as Y')
                return False
            else: 
                X = X * NY #extends the X list to match the size of the Y list
        return NX, NY, X, Y
    
    def plotting(self):
        NX, NY, self.xval, self.yval = self.pretreat(self.xval, self.yval)    
        f = plt.figure(figsize = self.figsize)
   
        for i in range(NY):
            plt.title(self.title, fontsize = self.fontsize * 1.1)
            plt.xlabel(self.xlabel, fontsize = self.fontsize)
            plt.ylabel(self.ylabel, fontsize = self.fontsize)
            plt.plot(self.xval[i], self.yval[i], self.marker, color = self.color_list[i],
                    linewidth = self.linewidth, label = self.label_list[i]) #overlays new curve on the plot
        if NY > 1:
            plt.legend()
        if self.date == True:            
            plt.savefig(str(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')) + self.save_name + self.extension)
        else: 
            plt.savefig(self.save_name + self.extension)
        return f
    
    def locator(self, x, axis_update):
        range_x = (x.max()-x.min())
        major_sample = range_x/self.sample
        minor_sample = major_sample / self.subsample
        
        majorLocator = MultipleLocator(major_sample)
        majorFormatter = FormatStrFormatter('%.1e')
        minorLocator = MultipleLocator(minor_sample)
        
        axis_update.set_major_locator(majorLocator)
        axis_update.set_major_formatter(majorFormatter)
        # for the minor ticks, use no labels; default NullFormatter
        axis_update.set_minor_locator(minorLocator)
    
    def logplot(self, x, y, color, label, log = ''):
            if log == 'loglog':
                plt.loglog(x, y, color = color, linewidth = self.linewidth, label = label)
            elif log == 'semilogy':
                plt.semilogy(x, y, color = color, linewidth = self.linewidth, label = label)
            elif log == 'semilogx':
                plt.semilogx(x, y, color = color, linewidth = self.linewidth, label = self.label)
            else: 
                plt.plot(x, y, color = color, linewidth = self.linewidth, label = label)
    
    def coplotting(self):
        NX1, NY1, self.xval, self.yval= self.pretreat(self.xval, self.yval)        
        NX2, NY2, self.x2val, self.y2val = self.pretreat(self.x2val, self.y2val)        

        fig, ax1 = plt.subplots(figsize = self.figsize)
        self.locator(self.xval[0], ax1.xaxis)
        self.locator(self.yval[0], ax1.yaxis)
        
        ax1.set_xlabel(self.xlabel, fontsize = self.fontsize * 1.1)
        ax1.set_ylabel(self.ylabel, color=self.color_list[0], fontsize = self.fontsize * 1.1)
        
        ax1.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize, which = 'major', width = self.linewidth//2)
        ax1.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize//2, which ='minor', width = self.linewidth//2) 


        for i, y in enumerate(self.yval):
            x = self.xval[i]
            color = self.color_list[i]
            label = self.label_list[i]
            self.logplot(x, y, color, label, self.ylog)

        plt.legend(prop={'size': self.fontsize})



        ax2 = ax1.twinx()  # second axis on the right
        self.locator(self.y2val[0], ax2.yaxis) 

        ax2.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize, which = 'major', width = self.linewidth//2)
        ax2.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize//2, which ='minor', width = self.linewidth//2) 

        ax2.set_ylabel(self.y2label, color=self.color_list[1], fontsize = self.fontsize * 1.1)
        
        for i, y in enumerate(self.y2val):
            x = self.x2val[i]
            color = self.color_list[i+1]
            label = self.label2_list[i]
            self.logplot(x, y, color, label, self.y2log)
            
        plt.legend(prop={'size': self.fontsize})

        #fig.tight_layout()

        plt.show()
        return fig




class showclass(object):
    """This class contains functions that can show images and subplot several images (and save the plot)
    Input: x [array or list/tuple of arrays]: images to plot
    Output: plot of the image x or subplots of images xi"""

        
    def __init__(self):
        #imshow parameters
        self.figsize = (9, 6) #figure size
        self.fontsize = 13  #font size
        self.title = 'My Title' #figure title
        self.cmap = 'inferno'

        #multiple image imshow        
        self.title_item = ['MyLabel']
        self.title_list = self.title_item * 100
        self.col_num = 3
       
        #figure save parameters
        self.date = True #write date and time before figure name
        self.save_name = 'Figure' #setting the format!
        self.save_folder = 'alienlab_images/'
        self.extension = '.tiff'
        self.save_im = True

    def showing(self, x=None, y=None, showit = False):
        if type(x) != tuple and type(x) != list: #When there is only one image, convert it in a list element
            x = [x]
            
        N = len(x)

        COLS = self.col_num
        if N == 1: #when there is only one image
            ROWS, COLS = 1, 1
        elif N%COLS == 0: #when its a multiple of the number of columns expected, no extra row should be added
            ROWS = N//COLS
        else: 
            ROWS = N//COLS + 1 #extra row for  remaining figures otherwise    
            
        f = plt.figure(figsize = self.figsize)
        
        if showit == True:
            plt.ion()
            plt.show()
        
        for i in range(N):
            plt.subplot(ROWS, COLS, i+1)
            plt.imshow(x[i], cmap = self.cmap)
            plt.axis('off')
            plt.grid(False)
            plt.title(self.title_list[i], fontsize = self.fontsize) #update subfigure title
        
        if showit == True:
            plt.pause(0.01)
            input("Press [enter] to continue.")
        if self.save_im == True:
            if self.date == True:            
                plt.savefig(self.save_folder + str(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_')) + self.save_name + self.extension,
                            bbox_inches='tight', frameon = False) #save with the date and time befor the figure name
            else: 
                plt.savefig(self.save_folder + self.save_name + self.extension, bbox_inches='tight', frameon = False)

        return f