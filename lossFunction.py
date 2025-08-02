
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
freq = ntw.f  # in Hz
s11  = ntw.s[:,0,0]
s21  = ntw.s[:,0,1]


# ------ GENERATE LOSS FUNCTION ---------------


# ------ function generation part -------------
def bandpass_target(fc, f, bw):
    """
    Ideal band-pass magnitude target:
      – returns 1.0 when f is inside [fc–bw/2, fc+ bw/2]
      – returns 0.0 otherwise
    fc : center frequency (scalar)
    f  : array (or scalar) of frequencies
    bw : total pass-band width
    """
    mask = (f >= fc - bw/2) & (f <= fc + bw/2)
    return mask.astype(float)



def gaussian_filter_target(fc, f, sigma):
    """
    Gaussian‐shaped target centered at fc.
    f can be a scalar or NumPy array of frequencies.
    """
    return np.exp(-((f - fc)**2) / (2 * sigma**2))

#def reflection_function(f):
    #return np.zeros_like(f) - 30


# ------ find loss between two functions --------
#also for context I am going to do everything here on out w the assumption that a Gaussian filter will be designed first
#s21 comparison
f_min = 3e9
f_max = 7e9
f_c = 5e9
sigma = 0.5e9
samples = 201

frequency_band = np.linspace(f_min, f_max, samples)


s21_mag_sim = np.abs(s21)
target_function = np.abs(gaussian_filter_target(f_c, frequency_band, sigma))
simulation_in_dB = 20*np.log10(s21_mag_sim + 1e-12)
target_function = np.abs(gaussian_filter_target(f_c, frequency_band, sigma))
target_in_dB = 20*np.log10(target_function + 1e-12)
error = target_in_dB - simulation_in_dB
err_s21_n = error/np.max(np.abs(error))
MSE_s21 = np.mean(err_s21_n**2)



#s11 comparison

#s11_mag_sim = np.abs(s21)
#interp_s11 = np.interp(frequency_band, freq, s11_mag_sim)
#sim_in_dB = 20*np.log(interp_s11 + 1e-12)


#target_s11 = np.abs(reflection_function(frequency_band))
#target_dB = 20*np.log(target_s11 + 1e-12)
#err = target_dB - sim_in_dB

#err_s11_n = err/np.max(np.abs(err))
#MSE_s11 = np.mean(err_s11_n**2)

# ------- calculate MSE, normal error given weights --------
total_error = 1.0 * MSE_s21 #+ 0.5 * MSE_s11
print(total_error)

os.makedirs(os.path.dirname(txt_output), exist_ok=True)
path=f"/home/u6068690/ResearchProject/Arrangements/sim_{number}"
file = f"loss_{number}"
print(txt_output)
with open(os.path.join(path, file), 'w') as f:
    print("finsihjed writing")
    f.write(str(total_error))

print("yay")