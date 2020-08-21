# import modules
import os
import re
import datetime as dt
import pandas as pd
import numpy as np
from numpy import pi
from numpy.fft import fft, fftshift


def read_complex_fid(file_path, drop_points=69):
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
        # get a list of rats
        # rat_number_list.append(rat_number)
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