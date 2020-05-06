# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 16:31:31 2020

@author: alien
"""

import numpy as np
import alienlab.plot
X = np.linspace(0, 13, 1000)
Y = [np.cos(X), np.cos(2*X)]

p = alienlab.plot.PlotFigure()
p.label_list = ['w = 1', 'w = 2']
p.title = 'Example'
p.xlabel = 'x'
p.ylabel = 'y'

fig = p.plotting(X, Y)
p.save_folder = 'save_figures'
p.date = False
p.save_name = 'plot_cos'
p.extension = '.png'
p.saving(fig)
p.showing(fig)


W = np.linspace(0.001, 1000, 100000)
Ac = W /(W**2 + 1)
As = -1/(W**2 + 1)
A = np.sqrt(Ac**2 + As**2)
angle = np.arctan(As/Ac) * 180 / np.pi

p.xval = W
p.yval = A
p.x2val = W
p.y2val = angle
p.title = 'Bode plot'
p.xlabel = 'Frequency'
p.ylabel = 'Amplitude'
p.y2label = 'Phase'
p.label2_list = 'Phase'
p.label_list = ['Amplitude']
p.ylog = 'loglog'
p.y2log = 'semilogx'
fig = p.coplotting()
p.save_name = 'plot_bode'
p.saving(fig)
p.showing(fig)