# necessary packages

from numpy import inf
# Aquisition parameters:

# Data Path
# DATA_DIRECTORY = '/home/mehrdad//fmig/data/Perfusion/'
# DATA_DIRECTORY = '/Users/mehipour/Downloads/Bruker 3/Perfusion/'
# DATA_DIRECTORY = '/Volumes/Freedom 7/Work/UPenn/Other Data/Bruker/Bruker 3/Perfusion/'
DATA_DIRECTORY = '/Users/mehipour/Desktop/data/'

# Bandwidth
SW_HZ = 8012.82051282051

# center frequency 
CENTER_FREQ_MHZ = 161.990667492615
CENTER_PPM = -3

# points to remove from beginning of FID
POINTS_TO_REMOVE = 68

# fitting parameters
INIT_VALS = [0.4, 0.3, 0.4, 2, 1.2, \
             0.25, 0.8, 0.5, 0.9, 0.4, \
             -16.5, -10, -8, -7.5, -2.5, \
             0, 4, 5, 6.5, 6, \
             0.2, \
             0.4, 0, 0, 0, 0]

LOWER_BOUND = [0.1, 0., 0., 0., 0., \
               0.1, 0.1, 0.1, 0.1, 0., \
               -17, -10.5, -8.5, -8, -3, \
               -0.5, 3.5, 4.5, 6, 5.5, \
               0.1, \
               -1, -1e-2, -1e-2, -1e5, -1e-4]

UPPER_BOUND = [5., 2., 2., 5., 5., \
               2., 5., 5., 5., 3., \
               -16, -9.5, -7.9, -7, -2, \
               0.5, 4.5, 5.5, 7, 6.5, \
               0.6, \
               1, 1e-2, 1e-2, 1e-4, 1e-4]

BOUNDS = (LOWER_BOUND, UPPER_BOUND)