
from math import e
import numpy as np
import skrf as rf
import argparse
import os

# ------------- PARSE SO THAT WE CAN GET THE RIGHT NUMBER ------------------
parser = argparse.ArgumentParser(prog="LossFunction",
                                 description="is able to calculate loss given other files")
parser.add_argument("--id", type=int, dest="sim_id", required=True, help="keeps track of sim_id for whole simulation")
parser.add_argument("--infile", dest="results", required=True, help= "defines the results by which the MSE is calculated")
parser.add_argument("--outfile", dest="txt_output", required=True, help="defines the output that the file should be written to")
args = parser.parse_args()
number = args.sim_id
results = args.results
txt_output = args.txt_output
print(results)

# ------ PUT RESULTS IN ARRAY FORMAT -------------
ntw = rf.Network(results)
freq = ntw.f 
s_db = ntw.s_db
s11  = s_db[:,0,0]
s21  = s_db[:,1,0]


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


f_min = 3e9
f_max = 7e9
samples = 201

freqs = np.linspace(f_min, f_max, 201)
s21_db = np.interp(freqs, ntw.f, s_db[:, 1, 0])

f_specs = {
    'f_pass_min': 3e9,
    'f_pass_max': 4.8e9,
    'f_stop_min': 5.2e9,
    'passband_db_max': -0.5,
    'stopband_db_min': -11.0,
    'passband_weight': 0.5,
    'stopband_weight': 0.5
    }


total_error = calculate_lowpass_loss(freqs, s21_db, f_specs)
os.makedirs(os.path.dirname(txt_output), exist_ok=True)
path=f"/home/u6068690/12x8ResearchProject/Arrangements/sim_{number}"
file = f"loss_{number}"
print(txt_output)
with open(os.path.join(path, file), 'w') as f:
    print("finsihed writing")
    f.write(str(total_error))
