
from math import e
import numpy as np
import skrf as rf
import argparse
import os
import glob

def calculate_lowpass_loss(freq, s21_db, specs):
    #use numpy to create an arr of booleans
    passband_mask = (freq <= specs['f_pass_max'])
    stopband_mask = (freq >= specs['f_stop_min'])

    s21_passband = s21_db[passband_mask]
    passband_error = np.maximum(0, specs['passband_db_max'] - s21_passband)
    loss_s21_passband = np.mean(passband_error**2)

    s21_stopband = s21_db[stopband_mask]
    stopband_error = np.maximum(0, s21_stopband - specs['stopband_db_min'])
    loss_s21_stopband = np.mean(stopband_error**2)

    total_loss = specs['passband_weight'] * loss_s21_passband + specs['stopband_weight'] * loss_s21_stopband

    return total_loss

total_sims = 6800

f_specs = {
    'f_pass_min': 3e9,
    'f_pass_max': 4.8e9,
    'f_stop_min': 5.2e9,
    'passband_db_max': -1.0,
    'stopband_db_min': -11.0,
    'passband_weight': 0.5,
    'stopband_weight': 0.5
    }

f_min = 3e9
f_max = 7e9
samples = 201

freqs = np.linspace(f_min, f_max, 201)

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
    s21_db = np.interp(freqs, ntw.f, s_db[:, 1, 0])
    total_error = calculate_lowpass_loss(freqs, s21_db, f_specs)
    print(total_error)
    output_path = rf"/home/u6068690/12x8ResearchProject/Arrangements/newLosses/sim_{sim_id}"
    os.makedirs(output_path, exist_ok=True)
    file = f"loss_{sim_id}"
    with open(os.path.join(output_path, file), 'w') as f:
        f.write(str(total_error))

print(count)






