#GOAL: to create a file that can successfully run a CST simulation from top to bottom

# ---------- IMPORT NEW LIBRARIES --------------
import os
import time
import numpy as np
from cst.interface import get_application #unfortunately the CST Studio API requires a different 



# ---------- CREATE DIRECTORY STRUCTURE FOR SIMULATION -------------
number = 1 #this is a current placeholder and must be GLOBALLY UPDATED somehow as the amount of simulations is batched - figure out how to do so ASAP
CST_PATH      = r"X:\Pixelated_Filter_bARLA.cst"      
BASE_FOLDER = rf"X:\b-ARLA Chip Design\Arrangements\sim_{number}"
os.makedirs(BASE_FOLDER, exist_ok=True)   # <-- make directory if needed
MACRO_NAME    = "arrangementGenerator.py"

cst_de = cst.interface.DesignEnvironment()


#--- OPEN FILE, INITIALIZE CST ---------
mww_prj = cst_de.new_mws()
mws_prj.save(prj_file, allow_overwrite=True)






# ---- INITIALIZE SOLVER PARAMETERS ----



# ----- RUN THE MACRO, CREATE PIXELS, STORE ARRANGEMENT -----------
mws_prj.save(prj_file, allow_overwrite=True) #save my whole microwave studio project

with cst_de.quiet_mode_enabled():
    mws_prj.model3d.start_solver() #figure out what this quiet mode thing actually is

mws_prj.model3d.ReportInformation("This message is from Python, but passed to CST messages window to confirm running from the terminal")

while mws_prj.model3d.is_solver_running():

    solver_run_info = mws_prj.model3d.get_solver_run_info()
    print(f"Solver is {solver_run_info['state']}")
    time.sleep(15)


for message in mws_prj.get_messages():
    print(message['text'])

mws_prj.save(prj_file, include_results=True, allow_overwrite=True) 







app = get_application()              
proj = app.OpenFile(CST_PATH)       


import importlib.util

spec = importlib.util.spec_from_file_location("gen", MACRO_NAME)
gen  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gen)

matrix, vb_history = gen.generate()
proj.model3d.add_to_history(MACRO_NAME, vb_history)

# 5) save the JSON of the arrangement
json_path = os.path.join(OUTPUT_FOLDER, f"arr_{number}.json")
with open(json_path, "w") as f:
    json.dump(matrix, f)



proj.AddHistory(MACRO_NAME, matrix_macro)
proj.Rebuild()                      
proj.StartSimulation()
while proj.SimulationStatus() != "Finished":
    time.sleep(1)
sparam = proj.GetResult("S-Parameters")  # or however your CST API exposes it
touchstone_file = os.path.join(OUTPUT_FOLDER, "sparams.s2p")
sparam.ExportTouchstone(touchstone_file)

# ----- OBTAIN RESULTS, EXPORT RESULTS TO DIRECTORY ------------







# ------- CONFIRM SIMULATION FINISH ---------------



#Close project, finish simulation + output
proj.Close()
print(f"Done. Matrix + S2P are in {OUTPUT_FOLDER}") 

# Then later, save into that folder:
matrix_path = os.path.join(new_folder, "matrix.npy")
np.save(matrix_path, matrix)

touchstone_file = os.path.join(new_folder, "sparams.s2p")
sparam.ExportTouchstone(touchstone_file)
