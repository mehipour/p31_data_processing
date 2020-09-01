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
        self.sw = 8000
        self.original_fid = fid
        self.fid = fid
        self.np = self.fid.shape[0]
        self.baseline = np.zeros_like(self.fid)
        self.ppm = np.arange(0, self.np)
        self.get_spectrum()

    def get_spectrum(self):
        self.spectrum = fftshift(fft(self.fid))

    def normalize_spectrum(self, scale=10):
        self.spectrum = self.spectrum / max(self.spectrum) * scale
        
    def phase(self, ph0, ph1):
        idx = np.arange(0, self.np)
        dph0 = ph0 - self.ph0
        dph1 = ph1 - self.ph1
        self.spectrum = self.spectrum * np.exp(1j*(dph0 + dph1*idx))
        self.ph0 = ph0
        self.ph1 = ph1
        
    def line_broad(self, lb=30):
        idx = np.linspace(0, self.np, self.np)
        dlb = lb - self.lb
        self.fid = self.fid * np.exp(-dlb*idx/self.sw)
        self.get_spectrum()
        self.phase(self.ph0, self.ph1)
        self.lb = lb

    def remove_baseline(self, poly_order=24):
        x = np.real(self.spectrum)
        baseline_object = BaselineRemoval(x)
        Modpoly_output = baseline_object.ModPoly(poly_order)
        Imodpoly_output = baseline_object.IModPoly(poly_order)
        self.spectrum = baseline_object.ZhangFit()

    def show_fid(self):
        plt.plot(np.real(self.fid), label='real')
        plt.plot(np.imag(self.fid), label='imaginary')
        plt.legend()
        plt.show()
    
    def show_complex_spectrum(self, show_ppm=True):
        plt.plot(self.ppm, np.real(self.spectrum), label='real')
        plt.plot(self.ppm, np.imag(self.spectrum), label='imaginary')
        plt.legend()
        plt.xlim(20, -25)
        plt.show()
        
    def show_real_spectrum(self, show_ppm=True):
        plt.plot(self.ppm, np.real(self.spectrum), label='real')
        plt.legend()
        plt.xlim(20, -25)
        plt.show()
        
    def show_abs_spectrum(self, show_ppm=True):
        plt.plot(self.ppm, np.absolute(self.spectrum), label='magnitude')
        plt.legend()
        plt.xlim(20, -25)
        plt.show()

    def find_ppm(self, center_freq_mhz, center_ppm):
        bw = np.linspace(-self.sw/2, self.sw/2, self.np)
        self.ppm = bw / center_freq_mhz + center_ppm

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
        return ("ph0", "ph1", "ph", "lb", "np", "sw", "ppm",
                "fid", "original_fid", "spectrum", "baseline")


# # define Experiment object
# class EXPbject():
#     ''' Object to define experiment
#     '''
#     def __init__(self, fid):
#         pass
        