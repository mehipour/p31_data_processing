# import modules
import os
import re
import datetime as dt
import pandas as pd
import numpy as np
from numpy import pi, inf
from numpy.fft import fft, fftshift
from scipy.optimize import curve_fit


def read_complex_fid(file_path, drop_points=68):
    ''' reads complex fid from bruker file
    '''
    file_path = file_path + '/fid' 
    with open(file_path, mode='rb') as fp:
        data = np.fromfile(fp, np.int32)
    complex_fid = data[::2] + 1j*data[1::2]

    return complex_fid[drop_points:]


def find_scan_gain(file_path):
    ''' reads scan gain
    '''
    file_path = file_path + '/acqp'
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
        for line in lines:
            if '##$RG' in line:
                val = line.split('=')[1]
                return int(val)


def find_protocol_name(file_path):
    ''' reads protocol name
    '''
    file_path = file_path + '/acqp'
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines):
            if 'ACQ_protocol_name' in line:
                aux = lines[i+1].strip('<')
                aux = aux[::-1].strip('\n>')
                return aux[::-1]


def find_scan_time(file_path):
    ''' reads scan time
    '''
    file_path = file_path + '/acqp'
    with open(file_path, 'r') as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines):
            if 'OWNER' in line:
                exp_time = dt.datetime.strptime(lines[i+1][14:22], "%H:%M:%S")
                return exp_time


def find_all_protocols(main_path, good_rats):
    ''' find all 31P scans and exclude bad studies
    '''
    parent_dir = os.listdir(main_path)
    parent_dir.remove('.DS_Store')

    study_dictionary = {}
    for directory in parent_dir:
        rat_number = int(directory[-2:])
        # discard bad rats
        if rat_number not in good_rats:
            continue
        # read all experimetns and include 31P studies only
        for experiment in os.listdir(main_path + directory):
            if '31P' in experiment:
                # go through scans
                scan_list = []
                scan_path_list = []
                for scan in os.listdir(main_path + '/' + directory + '/' + experiment):
                    # only include numbered folders.
                    if scan.isdigit():
                        scan_path = main_path + '/' + directory + '/' + experiment + '/' + str(scan) 
                        # check protocol name
                        if find_protocol_name(scan_path) == 'SINGLEPULSE_31p':
                            scan_list.append(int(scan))
                            scan_path_list.append(scan_path)
                # study_dictionary[rat_number] = sorted(scan_list)
                study_dictionary[rat_number] = scan_path_list
    return study_dictionary


def nmr_peak_fit(x, p0, p1, p2, p3, p4, p5, p6, 
                 p7, p8, p9, p10, p11, p12, p13,
                 p14, p15, p16, p17, p18, p19, p20,
                 p21, p22, p23, p24, p25):
    ''' function to fit 10 lorentizans and a 4th order polynomial fit to the 31p spectra
    Args:
    Return:
    '''
    f = p0*p20 / ((x-p10)**2 + p20**2) + \
        p1*p20 / ((x-p11)**2 + p20**2) + \
        p2*p20 / ((x-p12)**2 + p20**2) + \
        p3*p20 / ((x-p13)**2 + p20**2) + \
        p4*p20 / ((x-p14)**2 + p20**2) + \
        p5*p20 / ((x-p15)**2 + p20**2) + \
        p6*p20 / ((x-p16)**2 + p20**2) + \
        p7*p20 / ((x-p17)**2 + p20**2) + \
        p8*p20 / ((x-p18)**2 + p20**2) + \
        p9*p20 / ((x-p19)**2 + p20**2) + \
        p21 + p22*x + p23*x**2 + p24*x**3 + p25*x**4
    return f


def nmr_peak_fit_wrapper(x, s, f, r, p):
    ''' wrapper function for the nmr_peak_fit to make its use easier
    '''
    p0, p1, p2, p3, p4 = s[0], s[1], s[2], s[3], s[4] 
    p5, p6, p7, p8, p9 = s[5], s[6], s[7], s[8], s[9]
    p10, p11, p12, p13, p14 = f[0], f[1], f[2], f[3], f[4] 
    p15, p16, p17, p18, p19 = f[5], f[6], f[7], f[8], f[9]
    p20 = r
    p21, p22, p23, p24, p25 = p[0], p[1], p[2], p[3], p[4] 

    return nmr_peak_fit(x, p0, p1, p2, p3, p4, p5, p6,
                        p7, p8, p9, p10, p11, p12, p13,
                        p14, p15, p16, p17, p18, p19, p20, 
                        p21, p22, p23, p24, p25)

# # correct baseline
# def correct_baseline(nmr_object, poly_order=24):
#     ''' takes spectrum object and returns the baseline corrected version.
#     '''
#     peak_idx = list(np.arange(350,550)) + list(np.arange(750,850)) + list(np.arange(950,1100)) + list(np.arange(1250,1500))
#     x = np.arange(0, nmr_object.np)
#     baseline_idx = list(set(x) - set(peak_idx))

#     y = np.real(nmr_object.phased_spectrum)
#     p = np.polyfit(x[baseline_idx], y[baseline_idx], poly_order)
#     baseline = np.polyval(p, x)

#     return y - baseline, baseline