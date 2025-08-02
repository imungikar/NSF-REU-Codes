from dask.distributed import Client, SSHCluster
import subprocess
import json
import csv
import paramiko
from concurrent.futures import ThreadPoolExecutor
import numpy
import pandas as pd
import glob

losses = {}
for path in glob.glob("/scratch/u6068690/loss_*.json"):
    sim_id = int(path.split("_")[-1].split(".")[0])
    losses[sim_id] = json.load(open(path))["loss"]

cumMatrix = numpy.zeros((48, 32))
df = pd.read_csv("X:\\b-ARLA Chip Design\\Arrangements\\losses.csv")

for sim_id in range(1, 1001):
    path = rf"X:/b-ARLA Chip Design/Arrangements/sim_{sim_id}/arr.json"
    with open(path, 'r') as jf:
        arr = json.load(jf)
    arr = np.array(arr)
    mask = df["sim_id"] == sim_id
    loss_num = df.loc[mask, "loss"].iloc[0]
    newarr = loss_num * arr
    cumMatrix = cumMatrix + newarr

mean_value_cumMatrix = cumMatrix.mean()

CRM = numpy.zeros(48, 32)

for i in range (0, 48):
    for j in range(0, 32):
        if(cumMatrix[i][j] > mean_value_cumMatrix):
            CRM[i][j] = 0
        else:
            CRM[i][j] = 1

out_path = rf"X:\b-ARLA Chip Design\CRM.json"
with open(out_path, 'w') as f:
    json.dumps(CRM, f)


