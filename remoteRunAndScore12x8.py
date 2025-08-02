import argparse
import subprocess
import json
import csv
import paramiko
from concurrent.futures import ThreadPoolExecutor
import os
import time
import sys
import shutil

#right off the bat the first issue was cst_design_environment not being recognized as a command, thus brekaing the file!



# ------------------------------------------------
def run_and_score(sim_id):
    base_dir = f"/scratch/u6068690/12x8/sim_{sim_id}/"
    second_made_dir =  f"/home/u6068690/12x8ResearchProject/Arrangements/sim_{sim_id}"

    try:
        if os.path.exists(base_dir):
            shutil.rmtree(base_dir)
        if os.path.exists(second_made_dir):
            shutil.rmtree(second_made_dir)
        os.makedirs(base_dir, exist_ok=True)
        os.makedirs(second_made_dir, exist_ok=True)
        subprocess.run(["cp", "-r",
                "/home/u6068690/Pixelated_Filter_bARLA_12x8",
                base_dir], check=True)
        subprocess.run(["cp", "/home/u6068690/Pixelated_Filter_bARLA_12x8.cst", base_dir])
        new_dir = os.path.join(base_dir, "Pixelated_Filter_bARLA_12x8")
        id_file_path = os.path.join(new_dir, "sim_id.txt")
        with open(id_file_path, 'w') as f:
            f.write(str(sim_id))
        print(f"[{sim_id}] Verifying file write on NFS...")
        verified = False
        max_retries = 10
        for i in range(max_retries):
            subprocess.run(["sync"], check=True)
            time.sleep(0.5)
            try:
                with open(id_file_path, 'r') as f:
                    content = f.read().strip()
                if content == str(sim_id):
                    print(f"[{sim_id}] Verification successful after {i+1} attempt(s).")
                    verified = True
                    break
                else:
                    print(f"[{sim_id}] Verification failed: content mismatch ('{content}' != '{sim_id}'). Retrying...")
            except FileNotFoundError:
                print(f"[{sim_id}] Verification failed: file not found yet. Retrying...")
            time.sleep(1)

        if not verified:
            raise RuntimeError(f"Could not verify sim_id file for sim {sim_id} after {max_retries} retries.")
        subprocess.run(["/usr/local/apps/CST_Studio/2025/cst_design_environment", "-m", "-f", "--rebuild", "-num-threads=8", "-project-file", rf"{base_dir}Pixelated_Filter_bARLA_12x8.cst"], #somehow I need to be able to put these files into the scratch directory of the CADE PCs...how do I do that?
                       cwd=base_dir, check=True) 
        s2p_result = os.path.join(base_dir, "Pixelated_Filter_bARLA_12x8/Result/TOUCHSTONE files/MWS-run-0001.s2p")
        subprocess.run([
            "python3", "/home/u6068690/Scripts/12x8Scripts/lossFunction12x8.py",
            "--id", str(sim_id),
            "--infile", s2p_result, 
            "--outfile", rf"/home/u6068690/12x8ResearchProject/Arrangements/sim_{sim_id}/loss_{sim_id}"
        ], check=True)
        out_path = rf"/home/u6068690/12x8ResearchProject/Arrangements/sim_{sim_id}/loss_{sim_id}"
        print(f"ran and scored {sim_id}")
        with open(out_path, 'r') as f:
            loss = f.read().strip()

        return float(loss)

    except (subprocess.CalledProcessError, RuntimeError) as e:
        print(f"Simulation {sim_id} failed and will be retried.")
        return 0.0;
    
# ---------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", dest="sim_id", type=int, required=True)
    args = parser.parse_args()
    max_attempts = 2
    final_loss = 0.0
    for attempt in range(max_attempts):
        print(f"Starting attempt {attempt+1}/{max_attempts} for sim_id {args.sim_id}.")
        final_loss = run_and_score(args.sim_id)
        if final_loss > 1.0:
            print(f"Success: Sim {args.sim_id} completed!")
            break
        else:
            print(f"Attempt {attempt+1}/{max_attempts} failed for sim id {args.sim_id}, and will now be redone")

    print(final_loss)
