import argparse
import subprocess
import json
import csv
import paramiko
from concurrent.futures import ThreadPoolExecutor
import os
import cst.interface
from cst.interface import get_current_project
import random


#right off the bat the first issue was cst_design_environment not being recognized as a command, thus brekaing the file!


def generate_pixel_history(sim_id):

    prj = get_current_project()

    brick_width = 0.2
    brick_height = 0.2
    brick_depth = 0.03556
    random.seed(sim_id)
    appendedStringHistory = []
    count = 0
    placed = False
    matrix = []

    for i in range(-24, 24):
        row = []
        for j in range(-16, 16):
            if(random.random()<0.5):
                placed = True
            if(placed):
                placed = False
                row.append(1)
                center_x = i*0.2 + 0.1
                center_y = j*0.2 + 0.1
                center_z = 0.77
                wx = brick_width/2
                wy = brick_height/2
                x0, x1 = center_x-wx, center_x+wx
                y0, y1 = center_y-wy, center_y+wy
                z0, z1 = center_z, center_z+brick_depth
                appendedStringHistory.append(f"""
    With Brick
        .Reset 
        .Name "brick_{count}" 
        .Component "pixels" 
        .Material "Copper (pure)"
        .Xrange "{x0}", "{x1}"
        .Yrange "{y0}", "{y1}"
        .Zrange "{z0}", "{z1}"
        .Create
    End With
    """)
                count += 1
            else:
                row.append(0)
        matrix.append(row)
    history_list = "\n".join(appendedStringHistory)


    #patch adding part of the macro

    patch_width = 0.1
    patch_height = 0.1
    pixelHistory = []
    count = 0

    for k in range(0, 46):
        for l in range(0, 30):
            if ((matrix[k][l]   == 1 and matrix[k+1][l+1] == 1 and
                 matrix[k+1][l] == 0 and matrix[k][l+1]   == 0)
             or
                (matrix[k][l]   == 0 and matrix[k+1][l+1] == 0 and
                 matrix[k+1][l] == 1 and matrix[k][l+1]   == 1)):
                center_x = -4.6 + 0.2*(k)
                center_y = -3.0 + 0.2*(l)
                center_z = 0.77
                px = patch_width/2
                py = patch_height/2
                x0, x1 = center_x - px, center_x + px
                y0, y1 = center_y - py, center_y + py
                z0, z1 = center_z, center_z+brick_depth
                pixelHistory.append(f"""
    With Brick
        .Reset 
        .Name "patch_{count}" 
        .Component "pixels" 
        .Material "Copper (pure)"
        .Xrange "{x0}", "{x1}"
        .Yrange "{y0}", "{y1}"
        .Zrange "{z0}", "{z1}"
        .Create
    End With

    SelectTreeItem "Components\\pixels\\patch_{count}"

    With Transform 
         .Reset 
         .Name "pixels:patch_{count}" 
         .Origin "Free" 
         .Center "{center_x}", "{center_y}", "{center_z}" 
         .Angle "0", "0", "45" 
         .MultipleObjects "False" 
         .GroupObjects "False" 
         .Repetitions "1" 
         .MultipleSelection "False" 
         .AutoDestination "True" 
         .Transform "Shape", "Rotate" 
    End With

    """)
                count += 1

    #unfortunately the weird diagonal part of the screipt

    if((matrix[0][11] == 0 and matrix[0][10] == 1)):
        center_x = -4.8
        center_y = -1.0
        center_z = 0.77
        px = patch_width/2
        py = patch_height/2
        x0, x1 = center_x - px, center_x + px
        y0, y1 = center_y - py, center_y + py
        z0, z1 = center_z, center_z+brick_depth
        pixelHistory.append(f"""
    With Brick
        .Reset 
        .Name "patch_{count}" 
        .Component "pixels" 
        .Material "Copper (pure)"
        .Xrange "{x0}", "{x1}"
        .Yrange "{y0}", "{y1}"
        .Zrange "{z0}", "{z1}"
        .Create
    End With

    SelectTreeItem "Components\\pixels\\patch_{count}"

    With Transform 
         .Reset 
         .Name "pixels:patch_{count}" 
         .Origin "Free" 
         .Center "{center_x}", "{center_y}", "{center_z}" 
         .Angle "0", "0", "45" 
         .MultipleObjects "False" 
         .GroupObjects "False" 
         .Repetitions "1" 
         .MultipleSelection "False" 
         .AutoDestination "True" 
         .Transform "Shape", "Rotate" 
    End With

    """)
        count += 1
    if(matrix[0][20]==0 and matrix[0][21] == 1):
        center_x = -4.8
        center_y = 1.0
        center_z = 0.77
        px = patch_width/2
        py = patch_height/2
        x0, x1 = center_x - px, center_x + px
        y0, y1 = center_y - py, center_y + py
        z0, z1 = center_z, center_z+brick_depth
        pixelHistory.append(f"""
    With Brick
        .Reset 
        .Name "patch_{count}" 
        .Component "pixels" 
        .Material "Copper (pure)"
        .Xrange "{x0}", "{x1}"
        .Yrange "{y0}", "{y1}"
        .Zrange "{z0}", "{z1}"
        .Create
    End With

    SelectTreeItem "Components\\pixels\\patch_{count}"

    With Transform 
         .Reset 
         .Name "pixels:patch_{count}" 
         .Origin "Free" 
         .Center "{center_x}", "{center_y}", "{center_z}" 
         .Angle "0", "0", "45" 
         .MultipleObjects "False" 
         .GroupObjects "False" 
         .Repetitions "1" 
         .MultipleSelection "False" 
         .AutoDestination "True" 
         .Transform "Shape", "Rotate" 
    End With

    """)
        count += 1
    if(matrix[47][11] ==0 and matrix[47][10] ==1):
        center_x = 4.8
        center_y = -1.0
        center_z = 0.77
        px = patch_width/2
        py = patch_height/2
        x0, x1 = center_x - px, center_x + px
        y0, y1 = center_y - py, center_y + py
        z0, z1 = center_z, center_z+brick_depth
        pixelHistory.append(f"""
    With Brick
        .Reset 
        .Name "patch_{count}" 
        .Component "pixels" 
        .Material "Copper (pure)"
        .Xrange "{x0}", "{x1}"
        .Yrange "{y0}", "{y1}"
        .Zrange "{z0}", "{z1}"
        .Create
    End With

    SelectTreeItem "Components\\pixels\\patch_{count}"

    With Transform 
         .Reset 
         .Name "pixels:patch_{count}" 
         .Origin "Free" 
         .Center "{center_x}", "{center_y}", "{center_z}" 
         .Angle "0", "0", "45" 
         .MultipleObjects "False" 
         .GroupObjects "False" 
         .Repetitions "1" 
         .MultipleSelection "False" 
         .AutoDestination "True" 
         .Transform "Shape", "Rotate" 
    End With

    """)
        count += 1
    if(matrix[47][20] == 0 and matrix [47][21] ==1):
        center_x = 4.8
        center_y = 1.0
        center_z = 0.77
        px = patch_width/2
        py = patch_height/2
        x0, x1 = center_x - px, center_x + px
        y0, y1 = center_y - py, center_y + py
        z0, z1 = center_z, center_z+brick_depth
        pixelHistory.append(f"""
    With Brick
        .Reset 
        .Name "patch_{count}" 
        .Component "pixels" 
        .Material "Copper (pure)"
        .Xrange "{x0}", "{x1}"
        .Yrange "{y0}", "{y1}"
        .Zrange "{z0}", "{z1}"
        .Create
    End With

    SelectTreeItem "Components\\pixels\\patch_{count}"

    With Transform 
         .Reset 
         .Name "pixels:patch_{count}" 
         .Origin "Free" 
         .Center "{center_x}", "{center_y}", "{center_z}" 
         .Angle "0", "0", "45" 
         .MultipleObjects "False" 
         .GroupObjects "False" 
         .Repetitions "1" 
         .MultipleSelection "False" 
         .AutoDestination "True" 
         .Transform "Shape", "Rotate" 
    End With

    """)
        count += 1

    pixel_history_list = "\n".join(pixelHistory)

    second_made_dir =  f"/home/u6068690/ResearchProject/Arrangements/sim_{sim_id}"
    os.makedirs(second_made_dir, exist_ok=True)
    path=second_made_dir
    file = f"ArrangementOfArray"
    with open(os.path.join(path, file), 'w') as f:
        for row in matrix:
            f.write(" ".join(str(v) for v in row) + "\n")

    fullHistoryList = appendedStringHistory + pixelHistory
    return "\n".join(fullHistoryList)





# ------------------------------------------------
def run_and_score(sim_id):
    base_dir = f"/scratch/u6068690/sim_{sim_id}/"
    os.makedirs(base_dir, exist_ok=True)
    second_made_dir =  f"/home/u6068690/ResearchProject/Arrangements/sim_{sim_id}"
    os.makedirs(second_made_dir, exist_ok=True)
    subprocess.run(["cp", "/home/u6068690/Pixelated_Filter_bARLA.cst", base_dir])


    # --- Step 1: Generate the geometry history ---
    arrangement = generate_pixel_history(sim_id)

    # --- Step 2: Open CST, add geometry, and save ---
    de = cst.interface.DesignEnvironment(withGui=False)
    prj = de.open_project(rf"{base_dir}Pixelated_Filter_bARLA.cst")
    prj.model3d.add_to_history(f"Generate Pixels for sim_{sim_id}", arrangement)
    prj.save()
    prj.close()

    # -------------------
    subprocess.run(["/usr/local/apps/CST_Studio/2025/cst_design_environment", "-m", "-f", "-num-threads=8", "-project-file", rf"{base_dir}Pixelated_Filter_bARLA.cst"], #somehow I need to be able to put these files into the scratch directory of the CADE PCs...how do I do that?
                   cwd=base_dir, check=True) #fix this command to use the cst_design_environment command
    #I also need to copy the cst file into the scratch directory successfully

    s2p_result = os.path.join(base_dir, "Pixelated_Filter_bARLA/Result/TOUCHSTONE files/MWS-run-0001.s2p")
    subprocess.run([
        "python3", "lossFunction.py",
        "--id", str(sim_id),
        "--infile", s2p_result, #curious whether I need to include the full path for this
        "--outfile", rf"/home/u6068690/ResearchProject/Arrangements/sim_{sim_id}/loss_{sim_id}"
    ], check=True)
    out_path = rf"/home/u6068690/ResearchProject/Arrangements/sim_{sim_id}/loss_{sim_id}"
    print(f"ran and scored {sim_id}")
    with open(out_path, 'r') as f:
        loss = f.read().strip()

    return float(loss)
# ---------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", dest="sim_id", type=int, required=True)
    args = parser.parse_args()
    print(run_and_score(args.sim_id))
