#!/usr/bin/env python3


import subprocess
import re
import datetime
import time

# Function to read the current crontab
def read_crontab():
    result = subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()

# Function to write to crontab
def write_crontab(lines):
    temp_file = "/tmp/updated_crontab"
    with open(temp_file, "w") as temp:
        temp.write("\n".join(lines) + "\n")
    subprocess.run(["crontab", temp_file])

# Function to comment out a line matching a pattern
def comment_line_in_crontab(pattern):
    current_crontab = read_crontab()
    updated_crontab = []
    for line in current_crontab:
        if re.search(pattern, line) and not line.strip().startswith("#"):
            updated_crontab.append(f"# {line}")
        else:
            updated_crontab.append(line)
    write_crontab(updated_crontab)

# Function to run a specific job
def run_job(job_command):
    try:
        subprocess.run(job_command, shell=True, check=True)
        print(f"Job executed successfully: {job_command}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute job: {e}")

# Patterns for the two jobs
job1_pattern = r"ansible-playbook rule_request_2.yml --vault-password-file nothing.sh --tags enable"
job2_pattern = r"ansible-playbook rule_request_2.yml --vault-password-file nothing.sh --tags disable"

# Extract commands for the jobs based on the patterns
current_crontab = read_crontab()
job1_command = next((line for line in current_crontab if re.search(job1_pattern, line) and not line.startswith("#")), None)
job2_command = next((line for line in current_crontab if re.search(job2_pattern, line) and not line.startswith("#")), None)

# Execute the first job and comment it out
if job1_command:
    run_job(job1_command)
    comment_line_in_crontab(job1_pattern)
    print(f"Commented out the first job: {job1_pattern}")

# Wait for the second job's scheduled time (assumes a short delay for simplicity)
print("Waiting for the second job to execute...")
time.sleep(60)  # Adjust based on your scheduling needs

# Execute the second job and comment it out
if job2_command:
    run_job(job2_command)
    comment_line_in_crontab(job2_pattern)
    print(f"Commented out the second job: {job2_pattern}")
