# import packages
import numpy as np
from numpy.fft import fft, fftshift
import matplotlib.pyplot as plt
from BaselineRemoval import BaselineRemoval


# define NMR object
class NMRObject():
    ''' Object to define and FID, its spectrum, its phase.
    '''
    def __init__(self, fid):
        self.ph0 = 0
        self.ph1 = 0
        self.lb = 0
        self.sw = 1000
        self.fid = fid
        self.fidlb = fid
        self.np = self.fid.shape[0]
        self.baseline = np.zeros_like(self.fid)
        self.spectrum = fftshift(fft(self.fid))
        self.phased_spectrum = self.spectrum
        self.clean_spectrum = self.spectrum

    def phase(self, ph0=0, ph1=0):
        self.ph0 = ph0
        self.ph1 = ph1
        idx = np.linspace(-np.floor(self.np/2), np.floor(self.np/2), self.np)
        self.phased_spectrum = self.spectrum * np.exp(1j*(self.ph0+self.ph1*idx))
        
    def line_broad(self, lb=20):
        idx = np.linspace(0, self.np, self.np)
        self.lb = lb
        self.fidlb = self.fid * np.exp(-self.lb*idx/self.sw)
        self.spectrum = fftshift(fft(self.fidlb))
        self.phase(self.ph0, self.ph1)

    def remove_baseline(self, poly_order=24):
        x = np.real(self.phased_spectrum)
        baseline_object = BaselineRemoval(x)
        Modpoly_output = baseline_object.ModPoly(poly_order)
        Imodpoly_output = baseline_object.IModPoly(poly_order)
        self.clean_spectrum = baseline_object.ZhangFit()

    def show_fid(self):
        plt.plot(np.real(self.fid), label='real')
        plt.plot(np.imag(self.fid), label='imaginary')
        plt.legend()
        plt.show()
    
    def show_complex_spectrum(self):
        plt.plot(np.real(self.phased_spectrum), label='real')
        plt.plot(np.imag(self.phased_spectrum), label='imaginary')
        plt.legend()
        plt.show()
        
    def show_real_spectrum(self):
        plt.plot(np.real(self.phased_spectrum), label='real')
        plt.legend()
        plt.show()
        
    def show_abs_spectrum(self):
        plt.plot(np.absolute(self.phased_spectrum), label='magnitude')
        plt.legend()
        plt.show()

    def __getattr__(self, name):
        if name == 'ph':
            return [self.ph0, self.ph1]
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        if name == 'ph':
            self.ph0 = value[0]
            self.ph1 = value[1]
        else:
            return super().__setattr__(name, value)

    def __dir__(self):
        return ("ph0", "ph1", "ph", "lb", "np", "sw", 
                "fid", "fidlb", "spectrum", "phased_spectrum", "baseline")


# define Experiment object
class EXPbject():
    ''' Object to define experiment
    '''
    def __init__(self, fid):
        pass
        