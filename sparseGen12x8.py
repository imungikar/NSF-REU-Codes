from cst.interface import get_current_project
import random
import json
import argparse
import os
import numpy as np
import subprocess

matrix = []
print("HELLO THIS IS RUNNIINGGGG!")
parser = argparse.ArgumentParser()
parser.add_argument("--id", dest="sim_id", type=int, required=True)
args = parser.parse_args()
sim_id = args.sim_id

threshold = random.random() * 0.2 + 0.4

for i in range(-6, 6):
    row = []
    for j in range(-4, 4):
        if(random.random()<threshold):
            row.append(1)
        else:
            row.append(0)
    matrix.append(row)
second_made_dir =  f"/home/u6068690/12x8ResearchProject/Arrangements/sim_{sim_id}"
os.makedirs(second_made_dir, exist_ok=True)
path=second_made_dir
file = f"ArrangementOfArray"
with open(os.path.join(path, file), 'w') as f:
    for row in matrix:
        f.write(" ".join(str(v) for v in row) + "\n")


base_dir = f"/scratch/u6068690/12x8/sim_{sim_id}/"
os.makedirs(base_dir, exist_ok=True)
subprocess.run(["cp", "-r",
            "/home/u6068690/Pixelated_Filter_bARLA_12x8",
            base_dir], check=True)
new_dir = os.path.join(base_dir, "Pixelated_Filter_bARLA_12x8")
file = f"ArrangementOfArray"
cool_path = os.path.join(new_dir, file)
print("should be old")
subprocess.run(["cat", cool_path])
with open(os.path.join(new_dir, file), 'w') as f:
    for row in matrix:
        f.write(" ".join(str(v) for v in row) + "\n")

#with open(os.path.join("/home/u6068690/Pixelated_Filter_bARLA_12x8", file), 'w') as f:
#    for row in matrix:
#        f.write(" ".join(str(v) for v in row) + "\n")

print("should be new")
subprocess.run(["cat", cool_path])

id_file_path = os.path.join(new_dir, "sim_id.txt")
with open(id_file_path, 'w') as f:
    f.write(str(sim_id))