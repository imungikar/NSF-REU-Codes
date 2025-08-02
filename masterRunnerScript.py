from calendar import c
import subprocess
import json
import csv
import paramiko
from concurrent.futures import ThreadPoolExecutor
import os
import time
import math


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


    
NUM_SIMS     = 100            # total sims
hosts = [h for h, ok in results if ok]
chosen_hosts = hosts[0:15]
N_hosts = len(chosen_hosts)
print(chosen_hosts)

# def launch_sim(host, sim_id):
    #ssh = paramiko.SSHClient()
    #ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.connect(host, username=USER, timeout=5)
    #ssh.exec_command(f"mkdir -p /home/u6068690/logs/{sim_id}/{host}")
    #cmd = (
     #   f"source /home/u6068690/.tcshrc; "
     #   f"python3 /home/u6068690/Scripts/remoteRunAndScore.py --id {sim_id}"
    #)
    #ssh.exec_command(cmd)
    #ssh.close() 

def launch_sim(host, sim_id):
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=USER, timeout=5)
        ssh.exec_command(f"mkdir -p /home/u6068690/logs/{sim_id}/{host}")
        cmd = (
            f"source /home/u6068690/.tcshrc; "
            f"python3 /home/u6068690/Scripts/remoteRunAndScore.py --id {sim_id}"
        )
        stdin, stdout, stderr = ssh.exec_command(cmd)

        exit_status = stdout.channel.recv_exit_status()

        if exit_status == 0:
            print(f"Sim {sim_id} on {host} completed successfully.")
        else:
            print(f"Error on {host} for sim {sim_id}. Exit status: {exit_status}")
            print(stderr.read().decode())

    except Exception as e:
        print(f"Failed to run sim {sim_id} on {host}: {e}")
    finally:
        ssh.close()


START_SIM_ID = 1700
STAGGER = 5
batch_size = len(chosen_hosts)
all_sim_ids = range(START_SIM_ID, NUM_SIMS + START_SIM_ID)
num_batches = math.ceil(NUM_SIMS / batch_size)

for i in range(num_batches):
    start_idx = i*batch_size
    end_idx = start_idx + batch_size
    current_batch_ids = list(all_sim_ids)[start_idx:end_idx]
    with ThreadPoolExecutor(max_workers=N_hosts) as pool:
        tasks = []
        for j, sim_id in enumerate(current_batch_ids):
            host = chosen_hosts[j % N_hosts]
            tasks.append(pool.submit(launch_sim, host, sim_id))
            print(f"Submitting sim {sim_id} to {host}")
            time.sleep(STAGGER)

    print(tasks)
    for t in tasks:
        try:
            t.result()
        except Exception as e:
            print(f"A task in batch {i+1} failed: {e}")
            
    print(f"Batch {i+1} is complete out of {num_batches}")
    for sim_id in current_batch_ids:
        result_file = os.path.join("/home/u6068690/ResearchProject/Arrangements/", f"sim_{sim_id}/", f"loss_{sim_id}")
        try:
            with open(result_file, 'r') as f:
                loss_value = f.read().strip()
            print(f"{sim_id}\t\t{loss_value}")
        except FileNotFoundError:
            print(f"{sim_id}\t\tFAILED (No result file found)")
        except Exception as e:
            print(f"{sim_id}\t\tERROR reading result file: {e}")

print("\n--- FINAL RESULTS SUMMARY ---")
print("Sim ID\t\tLoss Value")
print("------\t\t----------")

for sim_id in all_sim_ids:
    result_file = os.path.join("/home/u6068690/ResearchProject/Arrangements/", f"sim_{sim_id}/", f"loss_{sim_id}")
    try:
        with open(result_file, 'r') as f:
            loss_value = f.read().strip()
        print(f"{sim_id}\t\t{loss_value}")
    except FileNotFoundError:
        print(f"{sim_id}\t\tFAILED (No result file found)")
    except Exception as e:
        print(f"{sim_id}\t\tERROR reading result file: {e}")

print("batch of many simulations complete")



