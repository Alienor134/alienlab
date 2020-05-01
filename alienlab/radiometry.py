import numpy as np
import alienlab.plot as alien
import matplotlib.pyplot as plt


class LED:
    """ power spectra and intensity graphs from LED specs: 
    - central wavelength (nm)
    - spectral bandwidth (nm)
    - optical power (mW)
    - half-view angle (°)"""
    
    def __init__(self, cw, bw, angle, power):
        self.cw = cw
        self.bw = bw
        self.angle = angle * np.pi / 180 
        self.power = power
        self.X = np.linspace(300, 800, 1000)
        self.eins = 100 * self.cw / 12
        
    def gaussian(self,x, mu, sig, power):
        return power * np.exp(-(x - mu)**2/(2 * sig**2)) / (sig * np.sqrt(2. * np.pi))

    def spectrum(self, plot = True):
        #power spectrum. Integral of spectrum equal to optical power.
        self.Y = self.gaussian(self.X, self.cw, self.bw, self.power)
        if plot == True:
            g = alien.PlotFigure()
            g.xlabel = "wavelength (nm)"
            g.ylabel = "Amplitude (mW/nm)"
            g.figsize = (5,5)
            g.marker = ''
            g.title = 'Power spectrum'
            g.plotting(self.X, self.Y)
        return self.Y
    
    def intensity(self, D, plot = True):
        # Variation of itensity with distance vs illumination field with distance
        self.S = np.pi * (D * np.tan(self.angle))**2
        self.I = (self.power/self.S) * self.eins
        if plot == True:
            g = alien.PlotFigure()
            g.figsize = (10, 5)
            g.xval = D
            g.yval = self.I
            g.x2val = D
            g.y2val = self.S
            g.ylabel = "Intensity (µE/m²/s)"
            g.xlabel = ("distance (mm)")
            g.label2_list = "Surface illuminated"
            g.label_list = "Intensty"
            g.y2label = "Surface illuminated (mm²)" 
            g.sample = 10
            g.subsample = 2
            g.ylog = 'loglog'
            g.y2log = 'loglog'
            g.coplotting()
        return self.S, self.I
    
    def surface(self, target_intensity, target_power):
        S = (target_power/target_intensity) * self.eins
        D = np.sqrt(S/np.pi)/np.tan(self.angle)
        return S, D
    def puissance(self, target_intensity, target_surface):
        return target_intensity * target_surface / self.eins
        