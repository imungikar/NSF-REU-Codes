import subprocess
import json
import csv
import numpy as np
import pandas as pd
import os

total_sim_ids = 5500

CRM = np.zeros((12,8))

for sim_id in range(1, total_sim_ids):
    path = rf"/home/u6068690/12x8ResearchProject/Arrangements/sim_{sim_id}/"
    matrix_path = os.path.join(path, "ArrangementOfArray")

    path2 = rf"/home/u6068690/12x8ResearchProject/Arrangements/newLossesWS1/sim_{sim_id}/"
    loss_path = os.path.join(path2, rf"loss_{sim_id}")
    if not os.path.exists(matrix_path) or not os.path.exists(loss_path):
        continue #this or break?
    
    with open(matrix_path, 'r') as f:
        mat = np.loadtxt(f)

    loss_sim = 0
    with open(loss_path, 'r') as f:
        loss_sim = float(f.read().strip())

    CRM += mat * loss_sim

mean_CRM = CRM.mean()
returnMatrix = np.zeros((12,8))

for i in range (0, 12):
    for j in range(0, 8):
        if(CRM[i][j] > mean_CRM):
            returnMatrix[i][j] = 0
        else:
            returnMatrix[i][j] = 1

out_path = rf"/home/u6068690/7KsimsCRMp5.txt"
with open(out_path, 'w') as f:
    np.savetxt(out_path, returnMatrix, fmt='%d', delimiter=' ')


subprocess.run(["cat", out_path])
