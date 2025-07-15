from tkinter import END
from dask.distributed import Client, SSHCluster
import subprocess
import json
import csv
import paramiko
from concurrent.futures import ThreadPoolExecutor
import numpy
import pandas as pd

cumMatrix = numpy.zeros(48, 32)
df = pd.read_csv("X:\\b-ARLA Chip Design\\Arrangements\\losses.csv")

for sim_id in range(1, 1001):
    arr = json.loads(rf"X:\b-ARLA Chip Design\Arrangements\sim_{sim_id}\arr_{sim_id}.json")
    loss_num = (df["sim_id"] == sim_id)["loss"]
    newarr = loss_num * arr
    cumMatrix = cumMatrix + newarr

mean_value_cumMatrix = cumMatrix.mean()

CRM = numpy.zeros(48, 32)

for i in range (0, 48):
    for j in range(0, 32):
        if(cumMatrix[i][j] < mean_value_cumMatrix):
            CRM[i][j] = 0
        else :
            CRM[i][j] = 1

out_path = rf"X:\b-ARLA Chip Design\CRM.json"

with(out_path, 'w') as f:
    json.dumps(CRM, f)


