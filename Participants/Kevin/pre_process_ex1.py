"""

Created on Wed Apr 22 17:47:23 2020
@author: Kevin MAchado Gamboa
AI Diagnostics Hackathon - Fundamental Respiration Sound

Ref:
    Kaggle:
        
    Librosa demo:
        https://nbviewer.jupyter.org/github/librosa/librosa/blob/master/examples/LibROSA%20demo.ipynb
"""
import aidiagnostics_toolbox as aidt

import numpy as np
import librosa as lb
from tqdm import tqdm
import soundfile as sfile
# And the display module for visualization
import librosa.display
import matplotlib.pyplot as plt
#%matplotlib inline
from scipy.io import wavfile as wf

# getting file path
from os.path import dirname as up
mf_path = up(up(up(__file__))).replace('\\','/')    # Main Folder Path
# changing to database path
import os
import glob
os.chdir(mf_path + '/Respiratory_Sound_Database/audio_and_txt_files')
# -----------------------------------------------------------------------------
#                              Data Loading
# -----------------------------------------------------------------------------
# Initializing Variables
sound_list = []
sound_reco = []
sf_reco = []
# Loading Loop
for file in tqdm(glob.glob("*.wav")):
    sound_list.append(file)
    # Loading and resampling sounds to 2kHz with librosa is too slow
    # data, sf = lb.load(mf_path + '/Respiratory_Sound_Database/audio_and_txt_files/' + file, sr = 2000)
    data, sf = sfile.read(mf_path + '/Respiratory_Sound_Database/audio_and_txt_files/' + file)
    # Signal Basic Preprocess
 #   data, sf = aidt.pre_pro_audio_PCG(data, sf)
    sound_reco.append(data)
    sf_reco.append(sf)
    
print(' -----')
n_sounds = np.shape(sound_list)[0]
print('Number of sound Recordings = ', n_sounds)

# selecting a single recording for the example
X = sound_reco[1]
X = aidt.butter_bp_fil(X, 100, 300, sf)
#%%
# -----------------------------------------------------------------------------
#                          Mel Spectrogram
# -----------------------------------------------------------------------------
# Let's make and display a mel-scaled power (energy-squared) spectrogram
S = lb.feature.melspectrogram(X, sr=sf, n_mels=128)
# Convert to log scale (dB). We'll use the peak power (max) as reference.
log_S = lb.power_to_db(S, ref=np.max)
# Make a new figure
plt.figure(figsize=(12,4))
plt.subplot(2,1,1)
# Display the spectrogram on a mel scale
# sample rate and hop length parameters are used to render the time axis
lb.display.specshow(log_S, sr=sf, x_axis='time', y_axis='mel')
# Put a descriptive title on the plot
plt.title('mel power spectrogram')
# draw a color bar
#plt.colorbar(format='%+02.0f dB')
plt.subplot(2,1,2)
# plot soundwave
plt.plot(512+(1000*X))
# Make the figure layout compact
plt.tight_layout()
#%%
# -----------------------------------------------------------------------------
#                     Harmonic-percussive source separation
# -----------------------------------------------------------------------------
y_harmonic, y_percussive = lb.effects.hpss(X)
# What do the spectrograms look like?
# Let's make and display a mel-scaled power (energy-squared) spectrogram
S_harmonic   = librosa.feature.melspectrogram(y_harmonic)#, sr=sf)
S_percussive = librosa.feature.melspectrogram(y_percussive)#, sr=sf)

# Convert to log scale (dB). We'll use the peak power as reference.
log_Sh = librosa.power_to_db(S_harmonic, ref=np.max)
log_Sp = librosa.power_to_db(S_percussive, ref=np.max)

# Make a new figure
plt.figure(figsize=(12,6))
plt.subplot(2,1,1)
# Display the spectrogram on a mel scale
librosa.display.specshow(log_Sh, sr=sf, y_axis='mel')
# Put a descriptive title on the plot
plt.title('mel power spectrogram (Harmonic)')
# draw a color bar
#plt.colorbar(format='%+02.0f dB')
plt.subplot(2,1,2)
librosa.display.specshow(log_Sp, sr=sf, x_axis='time', y_axis='mel')
# Put a descriptive title on the plot
plt.title('mel power spectrogram (Percussive)')
# draw a color bar
#plt.colorbar(format='%+02.0f dB')
# Make the figure layout compact
plt.tight_layout()

#%%
# -----------------------------------------------------------------------------
#                        Chromagram
# -----------------------------------------------------------------------------
# Make a new figure
plt.figure(figsize=(12,4))
#octa_vec = np.array([12, 24, 36, 48, 120, 180])
octa_vec = np.linspace(12, 12*15, 15)

k = len(octa_vec)
for i in range(k):
    plt.subplot(k,1,i+1)
    
    # We'll use a CQT-based chromagram with 36 bins-per-octave in the CQT analysis.  An STFT-based implementation also exists in chroma_stft()
    # We'll use the harmonic component to avoid pollution from transients
    C = librosa.feature.chroma_cqt(y=y_harmonic, sr=sf, bins_per_octave=int(octa_vec[i]))
    # Display the chromagram: the energy in each chromatic pitch class as a function of time
    # To make sure that the colors span the full range of chroma values, set vmin and vmax
    librosa.display.specshow(C, sr=sf, x_axis='time', y_axis='chroma', vmin=0, vmax=1)
    
    plt.title('Chromagram octaves %s' % str(octa_vec[i]))
#plt.colorbar()
plt.tight_layout()
#%%
# -----------------------------------------------------------------------------
#                          Beat tracking
# -----------------------------------------------------------------------------
# Now, let's run the beat tracker.
# We'll use the percussive component for this part
plt.figure(figsize=(12, 6))
tempo, beats = librosa.beat.beat_track(y=y_percussive, sr=sf)

# Let's re-draw the spectrogram, but this time, overlay the detected beats
plt.figure(figsize=(12,4))
librosa.display.specshow(log_S, sr=sf, x_axis='time', y_axis='mel')

# Let's draw transparent lines over the beat frames
plt.vlines(librosa.frames_to_time(beats),
            1, 0.5 * sf,
            colors='w', linestyles='-', linewidth=2, alpha=0.5)

plt.axis('tight')

plt.colorbar(format='%+02.0f dB')

plt.tight_layout();