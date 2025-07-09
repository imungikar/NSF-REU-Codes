from math import e
import numpy as np
import skrf as rf


# ------ PUT RESULTS IN ARRAY FORMAT -------------
ntw = rf.Network(r"X:\b-ARLA Chip Design\Arrangements\sim_{number}\arr_{number}.json")
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

def reflection_function(f):
    return 0


# ------ find loss between two functions --------
#also for context I am going to do everything here on out w the assumption that a Gaussian filter will be designed first
#s21 comparison
f_min = 3e9
f_max = 7e9
f_c = 5e9
sigma = 0.5
samples = 1000

frequency_band = np.linspace(f_min, f_max, samples)


s21_magnitude = np.abs(s21(frequency_band))
target_function = np.abs(gaussian_filter_target(f_c, frequency_band, sigma))

simulation_in_dB = 20*np.log(s21_magnitude)
target_in_dB = 20*np.log(target_function)

error = target_in_dB - simulation_in_dB

err_s21_n = error/np.max(np.abs(error))

MSE_s21 = np.mean(err_s21_n**2)



#s11 comparison
s11_magnitude = np.abs(s11(frequency_band))
target_s11 = np.abs(reflection_function(frequency_band))

sim_in_dB = 20*np.log(s11_magnitude)
target_dB = 20*np.log(target_s11)

err = target_dB - sim_in_dB

err_s11_n = err/np.max(np.abs(err))
MSE_s11 = np.mean(err**2)

# ------- calculate MSE, normal error given weights --------
total_error = 0.5 * MSE_s21 + 0.5 * MSE_s11
