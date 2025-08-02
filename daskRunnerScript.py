from dask.distributed import Client, SSHCluster
import subprocess
import json
import csv
import paramiko
from concurrent.futures import ThreadPoolExecutor
import os



# ----------- DEFINE MY WORKER MACHINES ----------
#need to find a way to see if worker uptime on a PC is particularly high or not
USER = "u6068690"
THRESHOLD = 1.3
possible_hosts = [f"lab1-{str(i)}.eng.utah.edu" for i in range(2,41)]


def possible_host(host: str) -> bool:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=USER, timeout=5)
        stdin, stdout, stderr = client.exec_command("uptime  | grep -oP '(?<=average:).*' | awk -F, '{ print $1 }'") #this has to be changed a little bit
        out = stdout.read().strip()
        uptime = float(out)
        return uptime < THRESHOLD
    except Exception as e:
        print(e)
        return False
    finally:
        client.close()

with ThreadPoolExecutor(max_workers=10) as worker_pool:
    results = worker_pool.map(lambda h: (h, possible_host(h)), possible_hosts)

hosts = [h for h, ok in results if ok]
print(hosts)
# ------------------------------------------------
scheduler = "lab1-1.eng.utah.edu"
worker_hosts = hosts
all_hosts = [scheduler] + worker_hosts

# ------- CREATE DASK SSH CLUSTER USING LIBRARY FEATURES ---------
cluster = SSHCluster(
    all_hosts,
    connect_options={"username": "u6068690", "known_hosts": None},
    worker_options={"nthreads": 1, "log_directory": "/scratch/u6068690/dask-logs"},     
    scheduler_options={"host": "0.0.0.0", "port": 0, "dashboard_address": ":8787"},
    remote_python="/home/u6068690/.vTest/bin/python3",
    env_extra="setenv LD_LIBRARY_PATH /usr/lib64/:"


)
client = Client(cluster)
print("Dask dashboard running at:", client.dashboard_link)

#making your own cluster = loop
# ----------------------------------------------------------------


# ------- DEFINE FUNCTIONS FOR A BATCHED SIMULATION PROCESS ---------
def run_and_score(sim_id):
    base_dir = f"/scratch/u6068690/sim_{sim_id}/"
    os.makedirs(base_dir, exist_ok=True)
    second_made_dir =  f"/home/u6068690/b-ARLA Chip Design/Arrangements/sim_{sim_id}"
    os.makedirs(second_made_dir, exist_ok=True)
    subprocess.run(["cp", "/home/u6068690/Pixelated_Filter_bARLA.cst", base_dir])
    subprocess.run(["cst_design_environment", "-m", "-f", "-num-threads=8", "-project-file", rf"{base_dir}Pixelated_Filter_bARLA.cst"], #somehow I need to be able to put these files into the scratch directory of the CADE PCs...how do I do that?
                   cwd=base_dir, check=True) #fix this command to use the cst_design_environment command
    #I also need to copy the cst file into the scratch directory successfully

    s2p_result = os.path.join(base_dir, "Pixelated_Filter_bARLA/Result/TOUCHSTONE files/MWS-run-0001.s2p")
    subprocess.run([
        "python3", "lossFunction.py",
        "--id", str(sim_id),
        "--infile", s2p_result, #curious whether I need to include the full path for this
        "--outfile", rf"X:/b-ARLA Chip Design/Arrangements/sim_{sim_id}/loss_{sim_id}.json"
    ], check=True)
    out_path = rf"X:/b-ARLA Chip Design/Arrangements/sim_{sim_id}/loss_{sim_id}.json"
    print(f"ran and scored {sim_id}")
    return json.loads(open(out_path).read())["loss"]
# --------------------------------------------------------------------



# -------- RUN 1000+ SIMULATIONS ON CLUSTER, GATHER RESULTS -------------
futures = [client.submit(run_and_score, sim_id) for sim_id in range(1, 1001)]
losses = client.gather(futures)

print("done gathering losses")


with open('X:\\b-ARLA Chip Design\\Arrangements\\losses.csv', 'w', newline ='\n') as newfile:
    writer = csv.writer(newfile)
    writer.writerow(["sim_id", "loss"])
    for sim_id, loss in enumerate(losses, start=1):
        writer.writerow([sim_id, loss])

print("Simulations finished. Analysis done. Ready to create CRM.")
# -----------------------------------------------------------------------


