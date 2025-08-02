#GOAL: to create a file that can successfully run a CST simulation from top to bottom

# ---------- IMPORT NEW LIBRARIES --------------
import os
import time
import numpy as np
import cst.interface
import refactorArrGen
import json
import argparse

parser = argparse.ArgumentParser(
    prog='run one CST sim',
    description='program actually runs one CST sim')
parser.add_argument("--id", dest="sim_id", type=int, required=True, help="Sim ID to keep track")
args = parser.parse_args()
number = args.sim_id


#create design environment
cst_de = cst.interface.DesignEnvironment()

#create string references for current directory, CST file to be used, and subsequent results directory
template      = r"X:\Pixelated_Filter_bARLA.cst"      
run_folder = rf"X:\b-ARLA Chip Design\Arrangements\sim_{number}"
os.makedirs(run_folder, exist_ok=True)   # <-- make directory if needed


#in this section you could add something to clean up other files and notebooks that you don't want - obviously as of rn not needed

# ---------------------------------------------------------------------------------------------------------------------------------


#copy my template and then subsequently continue my existing progress
import shutil

#fix w argparse later
run_id = 1
run_file = os.path.join(run_folder, f"sim_run_{run_id}.cst")
shutil.copyfile(template, run_file)

prj = cst_de.open_mws(run_file)
prj.save(run_file, allow_overwrite=True)

matrix, pixels_hist, patches_hist = refactorArrGen.generate_arrangement(seed = run_id)

json_path = os.path.join(run_folder f"arr_{number}.json")
with open(json_path, "w") as f:
    json.dump(matrix, f)

prj.model3d.add_to_history("Pixels added", pixels_hist)
prj.model3d.add_to_history("Patches added", patches_hist)


# ---- INITIALIZE SOLVER PARAMETERS ----


#first set units for the simulation/project
units_list = f"""
With Units
    .SetUnit "Length", "mm"
    .SetUnit "Temperature, "K"
    .SetUnit "Voltage", "V"
    .SetUnit "Current", "A"
    .SetUnit "Resistance", "Ohm"
    .SetUnit "Conductance", "S"
    .SetUnit "Capacitance", "pF"
    .SetUnit "Inductance", "nH"
    .SetUnit "Frequency", "GHz"
    .SetUnit "Time", "ns"
    .SetResultUnit "frequency", "frequency", ""
End With
"""
prj.model3d.add_to_history("Set units for solve", units_list)

#change the solver to what should be the right value WHICH I DO NOT KNOW YET FOR CONTEXT

prj.model3d.ChangeSolverType("Frequency Domain")


# ------- SET BOUNDARY CONDITIONS (DO NOT KNOW) -----------------------------------

boundary_list = f"""
With Boundary
    .Xmin "open" #figure out what this looks like
    .Xmax "expanded open"
    . etc etc etc
End With
"""

prj.model3d.add_to_history("Set boundary for solve")


# ------------ SET BACKGROUND (idk what exactly is going on) ----------------


# ----------- SET FREQUENCY RANGE -------
frequency_list = f"""
Solver.FrequencyRange "3", "7"
"""

prj.model3d.add_to_history("Define frequency range", frequency_list)





# ------- CONFIGURE MESH SETTINGS --------------

history_list = f"""
With Mesh 
     .MeshType "PBA" 
     .SetCreator "High Frequency"
End With

With MeshSettings 
     .SetMeshType "Hex" 
     .Set "Version", 1%
     'MAX CELL - WAVELENGTH REFINEMENT 
     .Set "StepsPerWaveNear", "15" 
     .Set "StepsPerWaveFar", "15" 
     .Set "WavelengthRefinementSameAsNear", "1" 
     'MAX CELL - GEOMETRY REFINEMENT 
     .Set "StepsPerBoxNear", "20" 
     .Set "StepsPerBoxFar", "1" 
     .Set "MaxStepNear", "0" 
     .Set "MaxStepFar", "0" 
     .Set "ModelBoxDescrNear", "maxedge" 
     .Set "ModelBoxDescrFar", "maxedge" 
     .Set "UseMaxStepAbsolute", "0" 
     .Set "GeometryRefinementSameAsNear", "0" 
     'MIN CELL 
     .Set "UseRatioLimitGeometry", "1" 
     .Set "RatioLimitGeometry", "20" 
     .Set "MinStepGeometryX", "0" 
     .Set "MinStepGeometryY", "0" 
     .Set "MinStepGeometryZ", "0" 
     .Set "UseSameMinStepGeometryXYZ", "1" 
End With 

With MeshSettings 
     .Set "PlaneMergeVersion", "2" 
End With

With MeshSettings 
     .SetMeshType "Hex" 
     .Set "FaceRefinementType", "NONE" 
     .Set "FaceRefinementRatio", "2" 
     .Set "FaceRefinementStep", "0" 
     .Set "FaceRefinementNSteps", "2" 
     .Set "EllipseRefinementType", "NONE" 
     .Set "EllipseRefinementRatio", "2" 
     .Set "EllipseRefinementStep", "0" 
     .Set "EllipseRefinementNSteps", "2" 
     .Set "FaceRefinementBufferLines", "3" 
     .Set "EdgeRefinementType", "RATIO" 
     .Set "EdgeRefinementRatio", "6" 
     .Set "EdgeRefinementStep", "0" 
     .Set "EdgeRefinementBufferLines", "3" 
     .Set "RefineEdgeMaterialGlobal", "0" 
     .Set "RefineAxialEdgeGlobal", "0" 
     .Set "BufferLinesNear", "3" 
     .Set "UseDielectrics", "1" 
     .Set "EquilibrateOn", "1" 
     .Set "Equilibrate", "1.5" 
     .Set "IgnoreThinPanelMaterial", "0" 
End With

With MeshSettings 
     .SetMeshType "Hex" 
     .Set "SnapToAxialEdges", "0"
     .Set "SnapToPlanes", "1"
     .Set "SnapToSpheres", "1"
     .Set "SnapToEllipses", "0"
     .Set "SnapToCylinders", "1"
     .Set "SnapToCylinderCenters", "1"
     .Set "SnapToEllipseCenters", "1"
     .Set "SnapToTori", "1"
     .Set "SnapXYZ" , "1", "1", "1"
End With

With Mesh 
     .ConnectivityCheck "True"
     .UsePecEdgeModel "True" 
     .PointAccEnhancement "0" 
     .TSTVersion "0"
	.PBAVersion "2024121625" 
     .SetCADProcessingMethod "MultiThread22", "-1" 
     .SetGPUForMatrixCalculationDisabled "False" 
End With
"""

prj.model3d.add_to_history("Python: set mesh properties (Hexahedral FIT)", history_list)

# ------------------ CONFIGURE SOLVER SETTINGS --------------------------
history_list = f"""
Mesh.SetCreator "High Frequency" 

With Solver 
     .Reset
     .Method "Hexahedral"
     .CalculationType "TD-S"
     .StimulationPort "All"
     .StimulationMode "All"
     .SteadyStateLimit "-40"
     .MeshAdaption "False"
     .AutoNormImpedance "False"
     .NormingImpedance "50"
     .CalculateModesOnly "False"
     .SParaSymmetry "False"
     .StoreTDResultsInCache  "True"
     .RunDiscretizerOnly "False"
     .FullDeembedding "False"
     .SuperimposePLWExcitation "False"
     .UseSensitivityAnalysis "False"
End With

"""

prj.model3d.add_to_history("Python: define time domain solver parameters", history_list)


#  -------------------- SAVE SIMULATION BEFORE STARTING --------------------------------------
prj.save(run_file, allow_overwrite=True)


# ------------------- ACTUALLY RUN THE SIMULATION AND PRINT THAT IT IS RUNNING
# Enable quiet mode to suppress GUI notifications and start the solver in non-blocking mode.
with cst_de.quiet_mode_enabled():
    prj.model3d.start_solver()

# Send a message to the CST Messages window from Python.
prj.model3d.ReportInformation("This message is from Python passed to the CST Messages window")

# While the solver is running, the script can continue executing other tasks.
# Here we run a loop that checks the solver's status at regular intervals.
while prj.model3d.is_solver_running():
    
    # Retrieve and display solver status information.
    solver_run_info = prj.model3d.get_solver_run_info()
    print(f"Solver is {solver_run_info['state']}")

    # Wait for 15 seconds before checking the solver status again.
    time.sleep(15)


# Once the solver has finished, retrieve and print the messages from the CST Messages window.
for message in prj.get_messages():
    print(message['text'])




# ----- RUN THE MACRO, CREATE PIXELS, STORE ARRANGEMENT -----------
prj.save(run_file, allow_overwrite=True) #save my whole microwave studio project

with cst_de.quiet_mode_enabled():
    prj.model3d.start_solver() #figure out what this quiet mode thing actually is

prj.model3d.ReportInformation("This message is from Python, but passed to CST messages window to confirm running from the terminal")

while prj.model3d.is_solver_running():

    solver_run_info = prj.model3d.get_solver_run_info()
    print(f"Solver is {solver_run_info['state']}")
    time.sleep(15)


for message in prj.get_messages():
    print(message['text'])

prj.save(run_file, include_results=True, allow_overwrite=True) 


# ----- IF I NEED A PARAMETER SWEEP I COULD IMPLEMENT IT HERE










# ------ DATA RETRIEVAL AND EXPORT (TO BE ANALYZED BY LOSS FUNCTION) -------------------

ts = prj.Touchstone          # now you have the full Touchstone interface
ts.Reset()
ts.FileName(f"X:\b-ARLA Chip Design\Arrangements\sim_{number}\touchstone.s2p")
ts.FrequencyRange("Full")
ts.Renormalize(True)
ts.Write()


# ------- CONFIRM SIMULATION FINISH ---------------
prj.Close()
print(f"Done. Matrix + S2P are in {run_folder}") 
