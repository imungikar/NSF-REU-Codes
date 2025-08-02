
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

def calculate_lowpass_loss(freq, s21_db,  specs):
    #use numpy to create an arr of booleans
    expectedValue = logistic_function(freq, specs['fc'], specs['k_21'], specs['Amin'], specs['Amax'])
    loss = np.abs(s21_db - expectedValue)
   # expectedValue2 = logistic_function(freq, specs['fc'], specs['k_11'], specs['Amin'], specs['Amax'])
   # loss2 = np.abs(s11_db - expectedValue2)
    MSE = np.mean(loss**4) #+ np.mean(loss2**2)

    return MSE

total_sims = 7000

f_specs = {
    'fc': 5,
    'k_21': 3,
    'k_11': -3,
    'Amin': -20.0,
    'Amax': -2.0,
    }

f_min = 3
f_max = 7
samples = 201

freqs_b4 = np.linspace(f_min, f_max, 201)
freqs = freqs_b4

count = 0
for sim_id in range(1, total_sims):
    s2pAnalysisPath = os.path.join(
            "/scratch/u6068690/12x8",
            f"sim_{sim_id}",
            "Pixelated_Filter_bARLA_12x8/Result/TOUCHSTONE files" #<-- Note: No backslash
        )    
    if not os.path.exists(s2pAnalysisPath):
        continue
    s2p_files = os.path.join(s2pAnalysisPath, 'MWS-run-0001.s2p')
    
    if not s2p_files:
        print(f"Warning: No .s2p file found in directory for sim_{sim_id}. Skipping.")
        count += 1
        continue # Skip to the next iteration
    ntw = rf.Network(s2p_files)
    freq = ntw.f 
    s_db = ntw.s_db
    s11  = s_db[:,0,0]
    s21  = s_db[:,1,0]
    s_db = ntw.s_db

    # Get frequency from the file AND CONVERT IT TO GHZ
    freq_from_file_ghz = ntw.f / 1e9 

    # Now both frequency arrays are in GHz, and interpolation works correctly
    #s11_db = np.interp(freqs, freq_from_file_ghz, s_db[:, 0, 0])
    s21_db = np.interp(freqs, freq_from_file_ghz, s_db[:, 1, 0])
    total_error = calculate_lowpass_loss(freqs, s21_db, f_specs)
    #if(total_error < 10.0):
    print(str(total_error) + " : " + str(sim_id))
    output_path = rf"/home/u6068690/12x8ResearchProject/Arrangements/newLossesWS1/sim_{sim_id}"
    os.makedirs(output_path, exist_ok=True)
    file = f"loss_{sim_id}"
    with open(os.path.join(output_path, file), 'w') as f:
        f.write(str(total_error))

print(count)






