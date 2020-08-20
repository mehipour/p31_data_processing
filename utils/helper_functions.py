# import packages
import os
import re
import numpy as np
from numpy import pi
from numpy.fft import fft, fftshift
import pandas as pd


# read fid
def read_complex_fid(file_path, drop_points=69):
    ''' reads complex fid from bruker file
    '''
    file_path = file_path + '/fid' 
    with open(file_path, mode='rb') as fp:
        data = np.fromfile(fp, np.int32)
    complex_fid = data[::2] + 1j*data[1::2]

    return complex_fid[drop_points:]


# read metafile
def find_31p_scan(file_path):
    ''' reads meta data
    '''
    file_path = file_path + '/acqp'
    pass



# correct baseline
def correct_baseline(nmr_object, poly_order=24):
    ''' takes spectrum object and returns the baseline corrected version.
    '''
    peak_idx = list(np.arange(350,550)) + list(np.arange(750,850)) + list(np.arange(950,1100)) + list(np.arange(1250,1500))
    x = np.arange(0, nmr_object.np)
    baseline_idx = list(set(x) - set(peak_idx))

    y = np.real(nmr_object.phased_spectrum)
    p = np.polyfit(x[baseline_idx], y[baseline_idx], poly_order)
    baseline = np.polyval(p, x)

    return y - baseline, baseline