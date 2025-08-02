from cst.interface import get_current_project
import random
import json
import argparse
import os
import numpy as np
from rich import print

print("BYEBYE THIS IS RUNNING TOO")
parser = argparse.ArgumentParser()
parser.add_argument("--id", dest="sim_id", type=int, required=True)
args = parser.parse_args()
sim_id = args.sim_id

pathOfArrangement  = f"/home/u6068690/ResearchProject/Arrangements/sim_{sim_id}/ArrangementOfArray"
arr = np.loadtxt(pathOfArrangement, dtype=int)

prj = get_current_project()
history_list = prj.modeler._GetHistory()

brick_width = 0.2
brick_height = 0.2
brick_depth = 0.03556

appendedStringHistory = []
count = 0
placed = False
matrix = []

for i in range(48):
    for j in range(32):
        if(arr[i, j]==1):
            placed = True
        if(placed):
            placed = False
            center_x = -4.7 + i*0.2
            center_y = -3.1 + j*0.2
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
history_list = "\n".join(appendedStringHistory)
print("bricks are done")

print(prj.modeler._GetHistory())

prj.model3d.add_to_history("Random pixel bricks", history_list)

#patch adding part of the macro

patch_width = 0.1
patch_height = 0.1
pixelHistory = []
count = 0

for k in range(0, 46):
    for l in range(0, 30):
        if ((arr[k, l]   == 1 and arr[k+1, l+1] == 1 and
             arr[k+1, l] == 0 and arr[k, l+1]   == 0)
         or
            (arr[k, l]    == 0 and arr[k+1, l+1]  == 0 and
             arr[k+1, l]  == 1 and arr[k, l+1]    == 1)):
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

if((arr[0, 11] == 0 and arr[0, 10] == 1)):
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
if(arr[0, 20]==0 and arr[0, 21] == 1):
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
if(arr[47, 11] ==0 and arr[47, 10] ==1):
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
if(arr[47, 20] == 0 and arr[47, 21] ==1):
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
print("patches are done")
prj.model3d.add_to_history("patches between set corners", pixel_history_list)

