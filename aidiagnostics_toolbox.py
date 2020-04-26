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
# -----------------------------------------------------------------------------
#                             Dataset Organization
# -----------------------------------------------------------------------------
from collections import Iterable                            # < py38
def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x

def elong_spec(in_list):
  matrix = np.zeros((in_list[0].shape[0], 1))
  for element in in_list:
    
    matrix = np.concatenate((matrix, element), axis=1)
  return matrix[:,1:]

def nn_org_dataset_spec(long_hs_vector, long_lb_vector, tc=0.1, fs=2000):
    '''
    organise dataset for NN
    input: 
        long_hs_vector: spectrogram matrix containing the whole recordings sticked to each other
        long_lb_vector: 1D array containing the whole labels sticked to each other
        tc: time-chunk 
    Functions Considerations
    ------------------------
    This function DISCARD the last samples of the input vector. This is because
    the # of examples per vector (ex) is usually not an int number
    '''
    
    chunks = int(fs*tc) # number of samples in a time 't' at 2kHz sampling freq.    
    ex = int(long_hs_vector.shape[1]/chunks) # Number of examples per vector
    mat_s = np.zeros((ex,long_hs_vector.shape[0],chunks))   # Spectrogram matrix
    mat_l = np.zeros((ex,chunks))   # Label matrix
    
    for i in range(ex):
        mat_s[i,:,:] = long_hs_vector[:,i*chunks:(1+i)*chunks]
        mat_l[i,:] = long_lb_vector[i*chunks:(1+i)*chunks]
    return mat_s, mat_l

def hs_longSpec(h_spec, h_labels, pc=0.70):
    '''
    Spec Long Matrices
    input: 
        h_spec: Heart sound spectrograms in a list (NxS) where N-> no. recordings; S-> no. samples per recording.
        h_labels: List (NxS) where N-> no. labels; S-> no. samples per label
        pc: percentage for training by each recording and label
    '''
    # Initializing train and test vectors
    train_s = []
    train_l = []
    test_s = []
    test_l = []
    # Loop for deviding between train and validation set
    for i in range(len(h_spec)):
        tr = int(h_spec[i].shape[1]*pc)     # number of samples per sound FOR TRAINING
        
        train_s.append(h_spec[i][:,:tr])  # sounds for training
        train_l.append(h_labels[i][:tr])  # labels for training
        test_s.append(h_spec[i][:,tr:])   # sounds for testing
        test_l.append(h_labels[i][tr:])   # labels for testing
    # Flatten the vectors    
    train_vectorS = elong_spec(train_s)
    print(train_vectorS.shape)
    train_vectorL = np.array(list(flatten(train_l)))
    print(train_vectorL.shape)
    test_vectorS = elong_spec(test_s)
    test_vectorL = np.array(list(flatten(test_l)))
    
    return train_vectorS, train_vectorL, test_vectorS, test_vectorL

def sq_labels_4(X):
    label_matrix = np.zeros([len(X), 3])
    for i in (range(len(X))):
        if round(np.mean(X[i,:])) == 0.0:
            label_matrix[i,0] = 1
        if round(np.mean(X[i,:])) == 1.0:
            label_matrix[i,1] = 1
        if round(np.mean(X[i,:])) == 2.0:
            label_matrix[i,2] = 1
    return label_matrix
