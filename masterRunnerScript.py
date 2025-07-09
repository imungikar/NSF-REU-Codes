import os
import time
import numpy as np
from cst.interface import get_application #unfortunately the CST Studio API requires a different
import paramiko
from concurrent.futures import ThreadPoolExecutor, as_completed

USER = "u6068690"
HOSTS = [f"{USER}.lab1@{number}.eng.utah.edu" for number in range(1, 21)]
KEY_PATH = "not sure yet"
CMD = "" #also need to figure out what commands are going to be run

#check for load on machine, create a set of the usable CADE machines

available_machines = []
for i in range(1, 21):
    if(less than a certain amount of load):
        available_machines.append(i)

#for machine in available_machines:


def run_on(host):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=USER, key_filename=KEY_PATH, timeout=10)
        stdin, stdout, stderr = client.exec_command(CMD)
        out = stdout.read().decode()
        err = stderr.read().decode()
        return host, out, err
    finally:
        client.close()

results = []
with ThreadPoolExecutor(max_workers=20) as pool:
    futures = { pool.submit(run_on, h): h for h in HOSTS }
    for fut in as_completed(futures):
        host, out, err = fut.result()
        print(f"[{host}] STDOUT:\n{out}")
        if err:
            print(f"[{host}] STDERR:\n{err}")
