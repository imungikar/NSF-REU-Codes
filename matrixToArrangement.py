from cst.interface import get_current_project
import random

#here we read into a matrix and then create the thing going on

prj = get_current_project()

brick_width = 0.2
brick_height = 0.2
brick_depth = 0.03556

appendedStringHistory = []
count = 0
placed = False
matrix = []

#matrix reading operation
import json
filename = f"arr_{number}.json"
with open(filename, "r") as fin:
    matrix = json.load(fin)

for i in range(0, 48):
    for j in range(0, 32):
        if(matrix[i][j]==1):
            center_x = -4.7 + 0.2*i 
            center_y = -3.1 + 0.2*j
            wx = brick_width/2
            wy = brick_height/2
            x0, x1 = center_x-wx, center_x+wx
            y0, y1 = center_y-wy, center_y+wy
            z0, z1 = center_z-wz, center_z+wz
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

history_list = "\n".join(appendedStringHistory)
prj.model3d.add_to_history("create the first part of the initial arrangement", history_list)

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
print(pixelHistory)
prj.model3d.add_to_history("patches for generated arranagement", pixel_history_list)
