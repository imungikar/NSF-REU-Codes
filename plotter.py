import numpy as np
import skrf as rf
import os
import matplotlib.pyplot as plt

# --- Data Loading ---
# NOTE: Ensure this path is correct for your system.
s2pAnalysisPath = os.path.join(
        "/home/u6068690/",
        "Pixelated_Filter_bARLA_12x8_Final5Ksims/Result/TOUCHSTONE files"
    )
s2p_files = os.path.join(s2pAnalysisPath, 'MWS-run-0001.s2p')

# Load the network data from the .s2p file
try:
    ntw = rf.Network(s2p_files)
except FileNotFoundError:
    print(f"Error: The file was not found at {s2p_files}")
    # Create dummy data to allow the script to run for demonstration
    freq = rf.Frequency(start=1, stop=10, npoints=101, unit='ghz')
    s11 = -20 * np.random.rand(101) - 10
    s21 = -1 * np.random.rand(101) - 0.5
    freq_ghz = freq.f_scaled
else:
    # Extract data from the file if found
    s_db = ntw.s_db
    freq_ghz = ntw.f / 1e9
    s11 = s_db[:,0,0] # Reflection coefficient
    s21 = s_db[:,1,0] # Transmission coefficient

# --- Create Two Separate, More Visible Plots ---
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10, 12))
label_fontsize = 14
tick_fontsize = 12

# -- Plot 1: S21 (Transmission) --
ax1.plot(freq_ghz, s21, label='$S_{21}$', color='royalblue', linewidth=2.5)
ax1.set_xlabel('Frequency (GHz)', fontsize=label_fontsize)
ax1.set_ylabel('Magnitude (dB)', fontsize=label_fontsize)
ax1.tick_params(axis='both', which='major', labelsize=tick_fontsize)
ax1.legend(fontsize=label_fontsize)
ax1.grid(True, which='both', linestyle='--')

# -- Plot 2: S11 (Reflection) --
ax2.plot(freq_ghz, s11, label='$S_{11}$', color='crimson', linewidth=2.5)
ax2.set_xlabel('Frequency (GHz)', fontsize=label_fontsize)
ax2.set_ylabel('Magnitude (dB)', fontsize=label_fontsize)
ax2.tick_params(axis='both', which='major', labelsize=tick_fontsize)
ax2.legend(fontsize=label_fontsize)
ax2.grid(True, which='both', linestyle='--')

# --- Dynamically Adjust Y-Axis Scale ---
s21_min, s21_max = np.min(s21), np.max(s21)
ax1.set_ylim(s21_min - 2, min(s21_max + 5, 0))

s11_min, s11_max = np.min(s11), np.max(s11)
ax2.set_ylim(s11_min - 2, min(s11_max + 5, 0))

# --- ADJUST SPACING AND DISPLAY PLOT ---
# Add vertical space between the top and bottom plots.
# hspace is the space as a fraction of the subplot height.
plt.subplots_adjust(hspace=0.3)

plt.show()