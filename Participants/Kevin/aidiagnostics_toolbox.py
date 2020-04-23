"""
AI Diagostics Ltd
@author: Kevin Machado

Created on Wed Apr  8 17:29:31 2020
Module file containing Python definitions and statements
"""

# Libraries
import numpy as np
from scipy import signal as sg
from scipy.signal import lfilter, butter


# -----------------------------------------------------------------------------
# 
# -----------------------------------------------------------------------------
def vec_nor(x):
    """
    Normalize the amplitude of a vector from -1 to 1
    """
    nVec = np.zeros(len(x));		   # Initializate derivate vector
    nVec = np.divide(x, max(x))
    nVec = nVec-np.mean(nVec);
    nVec = np.divide(nVec,np.max(nVec));
        
    return nVec
# -----------------------------------------------------------------------------
                             # PCG Audio Pre-Processing
# -----------------------------------------------------------------------------
def pre_pro_audio_PCG(x, fs):
# Ensure having a Mono sound
    if len(x.shape)>1:
    # select the left size
        x = x[:,0]
    # Resampling Audio PCG to 2k Hz
    Frs = 2000
    Nrs = int(Frs*(len(x)/fs)) # FsC  N; Fsn  x
    if fs > Frs:
        x = sg.resample(x, Nrs)
    
    return vec_nor(x), Frs
# -----------------------------------------------------------------------------
# Filter Processes
# -----------------------------------------------------------------------------
def butter_bp_coe(lowcut, highcut, fs, order=1):
    """
    Butterworth passband filter coefficients b and a
    Ref: 
    [1] https://timsainb.github.io/spectrograms-mfccs-and-inversion-in-python.html
    [2] https://gist.github.com/kastnerkyle/179d6e9a88202ab0a2fe
    """
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bp_fil(data, lowcut, highcut, fs, order=1):
    """
    Butterworth passband filter
    Ref: 
    [1] https://timsainb.github.io/spectrograms-mfccs-and-inversion-in-python.html
    [2] https://gist.github.com/kastnerkyle/179d6e9a88202ab0a2fe
    """
    b, a = butter_bp_coe(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return vec_nor(y)
