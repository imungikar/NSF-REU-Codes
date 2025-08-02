
from math import e
import numpy as np
import skrf as rf
import argparse
import os
import glob


def logistic_function(freq, fc, k, Amin, Amax):
    numerator = Amax - Amin
    denominator = 1 + np.exp(k * (freq - fc))
    return Amin + (numerator / denominator)

def calculate_lowpass_loss(freq, s21_db, s11db, specs):
    #use numpy to create an arr of booleans
    expectedValue = logistic_function(freq, specs['fc'], specs['k_21'], specs['Amin'], specs['Amax'])
    loss = np.abs(s21_db - expectedValue)
    expectedValue2 = logistic_function(freq, specs['fc'], specs['k_11'], specs['Amin'], specs['Amax'])
    loss2 = np.abs(s11_db - expectedValue2)
    MSE = np.mean(loss**4) + 0.5*np.mean(loss2**2)

    return MSE

simNumber = 1000

f_specs = {
    'fc': 5,
    'k_21': 3,
    'k_11': -3,
    'Amin': -20.0,
    'Amax': -0.5,
    }

f_min = 3
f_max = 7
samples = 201

freqs_b4 = np.linspace(f_min, f_max, 201)
freqs = freqs_b4

s2pAnalysisPath = os.path.join(
        "/home/u6068690/",
        "Pixelated_Filter_bARLA_12x8_Final5Ksims/Result/TOUCHSTONE files" #<-- Note: No backslash
    )    
s2p_files = os.path.join(s2pAnalysisPath, 'MWS-run-0001.s2p')
ntw = rf.Network(s2p_files)
freq = ntw.f 
s_db = ntw.s_db
s11  = s_db[:,0,0]
s21  = s_db[:,1,0]
# Get frequency from the file AND CONVERT IT TO GHZ
freq_from_file_ghz = ntw.f / 1e9 

# Now both frequency arrays are in GHz, and interpolation works correctly
s11_db = np.interp(freqs, freq_from_file_ghz, s_db[:, 0, 0])
s21_db = np.interp(freqs, freq_from_file_ghz, s_db[:, 1, 0])
total_error = calculate_lowpass_loss(freqs, s21_db, s11_db, f_specs)
print(total_error)

output_path = rf"/home/u6068690/12x8ResearchProject/Arrangements/testLossesp2/{simNumber}"
os.makedirs(output_path, exist_ok=True)
file = f"loss_{simNumber}"
with open(os.path.join(output_path, file), 'w') as f:
    f.write(str(total_error))







