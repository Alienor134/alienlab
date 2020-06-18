# -*- coding: utf-8 -*-


"""
Created on Thu Feb 14 22:29:53 2019

@author: Alienor Lahlou
"""




from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import datetime
from alienlab.utils import create_folder_if, random_color
import os
import numpy as np
import random
import pandas as pd




#Parent class

class Figure():
    def __init__(self):
        self.figsize = (9, 6)
        self.fontsize = 13
        self.title = 'My Title'
        
        #saving parameters
        self.save_folder = 'save_figures'
        
        self.date = True
        self.save_name = 'Figure'
        self.extension = '.tiff'

    
    def saving(self, f):
        create_folder_if(self.save_folder)
        
        if self.date == True:
            path = os.path.join(self.save_folder, str(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_')) + self.save_name)
        else:
            path = os.path.join(self.save_folder, self.save_name)
        try: 
            f[0].savefig(path + self.extension, bbox_inches='tight')
            f[1].to_csv(path + ".csv")
        except: 
            f.savefig(path + self.extension, bbox_inches='tight')

        return f
    
    def showing(self, f):
        plt.ion()
        try:
            f[0].show()
        except:
            f.show()    
        plt.pause(0.01)
        input("Press [enter] to continue.")
        return f        



#child class to ploth graphs
        
class PlotFigure(Figure):
    """This class contains functions that can plot graphs and several curves on a graph (and save the plot)
    Input: x [array or list/tuple of arrays]: x axis values, either one array or multiple arrays
    Input: y [array or list/tuple of arrays]: x axis values, either one array or multiple arrays
    Output: plot f(x) = y, or overlayed curves f(xi) = yi"""
        
    def __init__(self):
        super().__init__()
        #plot parameters
      
        self.color = 'steelblue'
        self.marker = 'o-'
        self.linewidth = 2
        self.legend = True #show legend for curves
        self.ticks = True   #not show ticks on the axis
        self.axes = False #not output the axes when plotting     
        
        #multiplot parameters
        self.label_item = ['MyLabel']
        self.label_list = self.label_item * 100
        self.color_list = [(1,0,0),(0,0,0),(0,0,1)] + [random_color(255) for i in range(100)]
        self.color2_list = [(0.5,0,0),(0.5,0.5,0.5),(0,0,0.5)] + [random_color(255) for i in range(100)]


        #[self.color] + ['indianred', 'seagreen', 'mediumslateblue', 'maroon', 'palevioletred'
                          #'orange', 'lightseagreen', 'dimgrey', 'slateblue']


        self.xval = []
        self.yval = []
        
        #axis formatting
        self.xlabel = 'x label (unit)'
        self.ylabel = 'y label (unit)'
        self.sample = 5
        self.subsample = 2
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
 

    def locator(self, mini, maxi, axis_update):
        range_x = maxi - mini
        major_sample = range_x/self.sample
        minor_sample = major_sample / self.subsample

        majorLocator = MultipleLocator(major_sample)
        majorFormatter = FormatStrFormatter('%.1e')
        minorLocator = MultipleLocator(minor_sample)

        axis_update.set_major_locator(majorLocator)
        axis_update.set_major_formatter(majorFormatter)
        # for the minor ticks, use no labels; default NullFormatter
        axis_update.set_minor_locator(minorLocator)

    def logplot(self, x, y, color, label,  log = '', linestyle = '-'):
            if log == 'loglog':
                plt.loglog(x, y, color = color, linewidth = self.linewidth, label = label, linestyle=linestyle)
            elif log == 'semilogy':
                plt.semilogy(x, y, color = color, linewidth = self.linewidth, label = label, linestyle=linestyle)
            elif log == 'semilogx':
                plt.semilogx(x, y, color = color, linewidth = self.linewidth, label = label, linestyle=linestyle)
            else: 
                plt.plot(x, y, color = color, linewidth = self.linewidth, label = label, linestyle=linestyle)
                
                
    def plotting(self, xval, yval):
        self.xval = xval
        self.yval = yval
        dict_for_pd = {}
        NX, NY, self.xval, self.yval = self.pretreat(self.xval, self.yval)    

        fig, ax1 = plt.subplots(figsize = self.figsize)
        
        if self.ticks == True:
            self.locator(np.array(self.xval).min(), np.array(self.xval).max(), ax1.xaxis)
            self.locator(np.array(self.yval).min(), np.array(self.yval).max(), ax1.yaxis)
        else: 
            ax1.tick_params(axis='both', top=False, bottom=False, left=False, right=False, labelleft=False, labelright = False, labelbottom=False)

        
        ax1.set_xlabel(self.xlabel, fontsize = self.fontsize * 1.1)
        ax1.set_ylabel(self.ylabel, color=self.color_list[0], fontsize = self.fontsize * 1.1)
        
        ax1.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize, which = 'major', width = self.linewidth//2)
        ax1.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize//2, which ='minor', width = self.linewidth//2) 

        for i in range(NY):
            plt.title(self.title, fontsize = self.fontsize * 1.1)
            plt.xlabel(self.xlabel, fontsize = self.fontsize)
            plt.ylabel(self.ylabel, fontsize = self.fontsize)
            self.logplot(self.xval[i], self.yval[i], color = self.color_list[i], label = self.label_list[i], log = self.ylog) #overlays new curve on the plot
            dict_for_pd[self.xlabel + ' ' + self.label_list[i]] = self.xval[i]
            dict_for_pd[self.ylabel + ' ' + self.label_list[i]] = self.yval[i]

        if NY > 1:
                if self.legend == True:
                        plt.legend(loc = 'best')


        df = pd.DataFrame.from_dict(dict_for_pd)

        if self.axes:
           return fig, ax1
        else:
            return fig, df


    
    def coplotting(self):
        NX1, NY1, self.xval, self.yval= self.pretreat(self.xval, self.yval)        
        NX2, NY2, self.x2val, self.y2val = self.pretreat(self.x2val, self.y2val)        
        dict_for_pd = {}

        fig, ax1 = plt.subplots(figsize = self.figsize)
       
        if self.ticks == True:
            self.locator(np.array(self.xval).min(), np.array(self.xval).max(), ax1.xaxis)
            self.locator(np.array(self.yval).min(), np.array(self.yval).max(), ax1.yaxis)                
        else: 
            ax1.tick_params(axis='both', top=False, bottom=False, left=False, right=False, labelleft=False, labelright = False,  labelbottom=False)
        
        ax1.set_xlabel(self.xlabel, fontsize = self.fontsize * 1.1)
        ax1.set_ylabel(self.ylabel, color=self.color_list[0], fontsize = self.fontsize * 1.1)
        
        ax1.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize, which = 'major', width = self.linewidth//2)
        ax1.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize//2, which ='minor', width = self.linewidth//2) 


        for i, y in enumerate(self.yval):
            x = self.xval[i]
            color = self.color_list[i]
            label = self.label_list[i]
            self.logplot(x, y, color, label, self.ylog, linestyle = '-')
            dict_for_pd[self.xlabel + ' ' + label] = self.xval[i]
            dict_for_pd[self.ylabel + ' ' + label] = self.yval[i]
        #plt.legend(loc = 'best', prop={'size': self.fontsize})



        ax2 = ax1.twinx()  # second axis on the right
        if self.ticks == True:
            self.locator(np.array(self.y2val).min(), np.array(self.y2val).max(), ax2.yaxis) 
        else: 
            ax2.tick_params(axis='both', top=False, bottom=False, left=False, right=False, labelleft=False, labelright = False,  labelbottom=False)
            

            
        ax2.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize, which = 'major', width = self.linewidth//2)
        ax2.tick_params(labelsize = self.fontsize * 0.8, length = self.fontsize//2, which ='minor', width = self.linewidth//2) 

        ax2.set_ylabel(self.y2label, color=self.color2_list[0], fontsize = self.fontsize * 1.1)
        
        for i, y in enumerate(self.y2val):
            x = self.x2val[i]
            color = self.color2_list[i]
            label = self.label2_list[i]
            self.logplot(x, y, color, label, log = self.y2log, linestyle = ":")
            dict_for_pd[self.xlabel + ' ' + label] = self.xval[i]
            dict_for_pd[self.y2label + ' ' + label] = self.yval[i]            
        #plt.legend(loc = 'best', prop={'size': self.fontsize})

        df = pd.DataFrame.from_dict(dict_for_pd)


        if self.axes:
           return fig, ax1, ax2

        else: 
           return fig, df


#Child class to plot images
class ShowFigure(Figure):
    """This class contains functions that can show images and subplot several images (and save the plot)
    Input: x [array or list/tuple of arrays]: images to plot
    Output: plot of the image x or subplots of images xi"""

        
    def __init__(self):
        super().__init__()
        #imshow parameters
        self.cmap = 'inferno'

        #multiple image imshow        
        self.title_item = ['MyLabel']
        self.title_list = self.title_item * 100
        self.col_num = 3
       
        #figure save parameters
        self.save_im = True
        self.spacing = 0.2

    def multi(self, x=None):
    
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
        
        for i in range(N):
            plt.subplot(ROWS, COLS, i+1)
            plt.imshow(x[i], cmap = self.cmap)
            plt.axis('off')
            plt.grid(False)
            plt.subplots_adjust(wspace=self.spacing, hspace=self.spacing)
            if self.title_list != None:
                plt.title(self.title_list[i], fontsize = self.fontsize) #update subfigure title
        
        return f
