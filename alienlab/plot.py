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
import matplotlib
from mpl_toolkits.axes_grid1 import make_axes_locatable

matplotlib.rcParams['font.sans-serif'] = "Arial"
matplotlib.rcParams['font.family'] = "sans-serif"


from collections import OrderedDict

linestyles = OrderedDict(
    [('solid',               (0, ())),
     #('loosely dotted',      (0, (1, 10))),
     ('dotted',              (0, (1, 2))),
     ('densely dotted',      (0, (1, 1))),

     #('loosely dashed',      (0, (5, 10))),
     ('dashed',              (0, (5, 2))),
     ('densely dashed',      (0, (5, 1))),

     #('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('dashdotted',          (0, (3, 2, 1, 2))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     #('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('dashdotdotted',         (0, (3, 2, 1, 2, 1, 2))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])
keys = list(linestyles.keys())

#Parent class

class Figure():
    def __init__(self):
        self.figsize = (9, 6)
        self.fontsize = 13
        self.fonttick = 12
        self.title = 'My Title'
        
        #saving parameters
        self.save_folder = 'save_figures'
        self.save_path = ""
        self.date = True
        self.save_name = 'Figure'
        self.extension = '.tiff'
        self.mongo = False
        self.mongo_run = False
        self.label_intensity = r"$I$ ($\mu E.m^{-2}.s^{-1}$)"
        self.label_tau = r"1/$\tau$ ($s^{-1}$)"
    
    def saving(self, f):
        create_folder_if(self.save_folder)
        
        if self.mongo == True:
            try:
                self.mongo_run != False
            except:
                print("if Mongo is True, you need to provide a _run. Setting mongo to False!")
                self.mongo = False

        if self.date == True:
            self.save_name = str(datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_')) + self.save_name

        self.save_path = os.path.join(self.save_folder, self.save_name)

        if type(f)==type(plt.figure()):

            f.savefig(self.save_path + self.extension)
            if self.mongo:
                self.mongo_run.add_artifact(self.save_path + self.extension)


        else: 
            f[0].savefig(self.save_path + self.extension)
            f[1].to_csv(self.save_path + ".csv")
            if self.mongo:
                self.mongo_run.add_artifact(self.save_path + self.extension)
                self.mongo_run.add_artifact(self.save_path + ".csv")



        
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
        self.marker_list = ['.']*100
        self.linestyle_list = ['-']*100
        self.linewidth = 2
        self.legend = True #show legend for curves
        self.ticks = True   #not show ticks on the axis
        self.axes = False #not output the axes when plotting
        self.majorFormatterx = "%0.3e"#"%0.2f"
        self.majorFormattery = "%0.3e"#"%0.2f"
        self.major_ticks = True     
        self.minor_ticks = False
        #multiplot parameters
        self.label_item = ['MyLabel']
        self.label_list = self.label_item * 100
        self.color_list = [(1,0,0),(0,0,0),(0,0,1)] + [random_color(255) for i in range(100)]
        self.color2_list = [(0.5,0,0),(0.5,0.5,0.5),(0,0,0.5)] + [random_color(255) for i in range(100)]
        self.linestyles = [linestyles[k] for k in keys]

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
        self.marker2_list = [""]*100
        self.linestyle2_list = [":"]*100
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
        range_array = maxi - mini
        major_sample = range_array/self.sample
        minor_sample = major_sample / self.subsample
        majorLocator = MultipleLocator(major_sample)

        majorFormatter = FormatStrFormatter('%.2f')
        minorLocator = MultipleLocator(minor_sample)

        if axis_update.__name__ == 'xaxis':
            majorFormatter = FormatStrFormatter(self.majorFormatterx)
        elif axis_update.__name__ == "yaxis":
            majorFormatter = FormatStrFormatter(self.majorFormattery)

        axis_update.set_major_locator(majorLocator)
        axis_update.set_major_formatter(majorFormatter)
        # for the minor ticks, use no labels; default NullFormatter
        if self.minor_ticks:
            axis_update.set_minor_locator(minorLocator)

    def logplot(self, x, y, color, marker, linestyle, label,  log = ''):
            if log == 'loglog':
                plt.loglog(x, y, marker = marker, linestyle = linestyle, color = color, linewidth = self.linewidth, label = label)
            elif log == 'semilogy':
                plt.semilogy(x, y, marker = marker, linestyle = linestyle, color = color, linewidth = self.linewidth, label = label)
            elif log == 'semilogx':
                plt.semilogx(x, y, marker = marker, linestyle = linestyle, color = color, linewidth = self.linewidth, label = label)
            else: 
                plt.plot(x, y, marker = marker, linestyle = linestyle, color = color, linewidth = self.linewidth, label = label)
                
                
    def set_figure(self, formatx="none" , formaty = "none"):
        if formatx == "none":
            formatx =self.majorFormatterx
        if formaty == "none":
            formaty =self.majorFormattery
            
        inch=2.54
        self.figsize = (13/inch,12/inch)
        self.fontsize = 18
        self.fonttick = 12
        rc = {"font.family" : "Arial", 
            "mathtext.fontset" : "dejavusans"}
        plt.rcParams.update(rc)
            
        fig = plt.figure(figsize = self.figsize)
        ax1 = plt.gca()
        ax1.set_xlabel(self.xlabel, fontsize = self.fontsize)
        ax1.set_ylabel(self.ylabel,fontsize = self.fontsize)
        ax1.tick_params(axis='both', top=False, bottom=True, left=True, right=False, labelleft=True, labelright = False,  labelbottom=True)
        ax1.tick_params(labelsize = self.fonttick, length = self.fonttick//2, which = 'major', width = self.linewidth//2, direction = 'in')
        ax1.tick_params(labelsize = self.fonttick*0, length = self.fonttick//4, which ='minor', width = self.linewidth//2, direction = 'in') 
        formatx = FormatStrFormatter(formatx)
        formaty = FormatStrFormatter(formaty)

        ax1.xaxis.set_major_formatter(formatx)
        ax1.yaxis.set_major_formatter(formaty)
        left = 2.5/inch/(self.figsize[0])
        top = 1 - 0.5/inch/(self.figsize[1])
        right = 1 - 0.5/inch/(self.figsize[0])
        bottom = 1.5/inch/(self.figsize[1])
        fig.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=None, hspace=None)
        return fig
    
    
    def image_scale(self, im, crop=False):
        if crop==True:
            Q1 = np.quantile(im, 0.01)
            Q3 = np.quantile(im, 0.95)
            im[im <= Q1 ] = Q1
            im[im >= Q3 ] = Q3
    
        fig = self.set_figure()
        image = plt.imshow((im))
        plt.axis("off")
        divider = make_axes_locatable(plt.gca())
        axdef = divider.append_axes("bottom", "5%", pad="3%")
        cbar = plt.colorbar(image, cax=axdef, orientation = "horizontal")
        cbar.ax.tick_params(labelsize=self.fontsize, size = self.fontsize/2, width = 2)
        return fig

    def plotting(self, xval, yval):
        self.xval = xval
        self.yval = yval
        dict_for_pd = {}
        NX, NY, self.xval, self.yval = self.pretreat(self.xval, self.yval)    

        fig, ax1 = plt.subplots(figsize = self.figsize)
        
        if self.ticks == True and len(self.xval) > 0 and len(self.yval) > 0:
            
            xx = np.concatenate(self.xval)
            yy = np.concatenate(self.yval)

            self.locator(xx.min(), xx.max(), ax1.xaxis)
            self.locator(yy.min(), yy.max(), ax1.yaxis)
        else: 
            ax1.tick_params(axis='both', top=False, bottom=False, left=False, right=False, labelleft=False, labelright = False, labelbottom=False)

        
        ax1.set_xlabel(self.xlabel, fontsize = self.fontsize)
        ax1.set_ylabel(self.ylabel, fontsize = self.fontsize)
        
        if self.major_ticks == True:
            ax1.tick_params(axis = 'x', labelsize = self.fonttick, length = self.fonttick, which = 'major', width = self.linewidth//2,
                            direction = 'in')
            ax1.tick_params(axis = 'y', labelsize = self.fonttick, length = self.fonttick, which = 'major', width = self.linewidth//2,

                            direction = 'in', top = True, right = True)
        if self.minor_ticks == True:
            ax1.tick_params(labelsize = self.fonttick, length = self.fonttick//2, which ='minor', width = self.linewidth//2,
                            direction = 'in') 

        for i in range(NY):
            plt.title(self.title, fontsize = self.fontsize * 1.1)
            plt.xlabel(self.xlabel, fontsize = self.fontsize)
            plt.ylabel(self.ylabel, fontsize = self.fontsize)
            color = self.color_list[i]
            label = self.label_list[i]
            marker = self.marker_list[i]
            linestyle = self.linestyle_list[i]
            self.logplot(self.xval[i], self.yval[i], marker = marker, linestyle = linestyle, color = color, label = label, log = self.ylog) #overlays new curve on the plot
            dict_for_pd[self.xlabel + ' ' + self.label_list[i]] = self.xval[i]
            dict_for_pd[self.ylabel + ' ' + self.label_list[i]] = self.yval[i]

        if NY > 1:
                if self.legend == True:
                        plt.legend(loc = 'best')

        def pad_dict_list(dict_list, padel):
            lmax = 0
            for lname in dict_list.keys():
                lmax = max(lmax, len(dict_list[lname]))
            for lname in dict_list.keys():
                ll = len(dict_list[lname])
                if  ll < lmax:
                    dict_list[lname] =  np.concatenate([np.array(dict_list[lname]), np.array([padel] * (lmax - ll))])
            return dict_list

        dict_for_pd = pad_dict_list(dict_for_pd, 0)

        df = pd.DataFrame.from_dict(dict_for_pd)

        if self.axes:
           return fig, ax1
        else:
            return fig, df, ax1


    
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
        
        ax1.set_xlabel(self.xlabel, fontsize = self.fontsize)
        ax1.set_ylabel(self.ylabel, color=self.color_list[0], fontsize = self.fontsize)
        
        ax1.tick_params(labelsize = self.fonttick, length = self.fonttick, which = 'major', width = self.linewidth//2)
        ax1.tick_params(labelsize = self.fonttick*0, length = self.fonttick//2, which ='minor', width = self.linewidth//2) 


        for i, y in enumerate(self.yval):
            x = self.xval[i]
            color = self.color_list[i]
            label = self.label_list[i]
            marker = self.marker_list[i]
            linestyle = self.linestyle_list[i]

            self.logplot(x, y, color, marker, linestyle, label, self.ylog)
            dict_for_pd[self.xlabel + ' ' + label] = self.xval[i]
            dict_for_pd[self.ylabel + ' ' + label] = self.yval[i]
        #plt.legend(loc = 'best', prop={'size': self.fontsize})



        ax2 = ax1.twinx()  # second axis on the right
        if self.ticks == True:
            self.locator(np.array(self.y2val).min(), np.array(self.y2val).max(), ax2.yaxis) 
        else: 
            ax2.tick_params(axis='both', top=False, bottom=False, left=False, right=False, labelleft=False, labelright = False,  labelbottom=False)
            

            
        ax2.tick_params(labelsize = self.fonttick, length = self.fonttick, which = 'major', width = self.linewidth//2)
        ax2.tick_params(labelsize = self.fonttick, length = self.fonttick//2, which ='minor', width = self.linewidth//2) 

        ax2.set_ylabel(self.y2label, color=self.color2_list[0], fontsize = self.fontsize)
        
        for i, y in enumerate(self.y2val):
            x = self.x2val[i]
            color = self.color2_list[i]
            label = self.label2_list[i]
            marker = self.marker2_list[i]
            linestyle = self.linestyle2_list[i]
            self.logplot(x, y, marker = marker, linestyle = linestyle, color=color, label=label, log = self.y2log)
            dict_for_pd[self.xlabel + ' ' + label] = self.xval[i]
            dict_for_pd[self.y2label + ' ' + label] = self.yval[i]            
        #plt.legend(loc = 'best', prop={'size': self.fontsize})

        def pad_dict_list(dict_list, padel):
            lmax = 0
            for lname in dict_list.keys():
                lmax = max(lmax, len(dict_list[lname]))
            for lname in dict_list.keys():
                ll = len(dict_list[lname])
                if  ll < lmax:
                    dict_list[lname] =  np.concatenate([np.array(dict_list[lname]), np.array([padel] * (lmax - ll))])
            return dict_list

        dict_for_pd = pad_dict_list(dict_for_pd, 0)
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
