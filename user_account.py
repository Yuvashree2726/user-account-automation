import csv
import secrets
import subprocess
from pathlib import Path

cwd = Path.cwd()

with open(cwd / "user_in.csv", "r") as file_input, open(cwd / "user_out.csv", "w") as file_output:
    reader = csv.DictReader(file_input)
    writer = csv.DictWriter(file_output, fieldnames=reader.fieldnames)
    writer.writeheader()

    for user in reader:
        user["password"] = secrets.token_hex(8)
        useradd_cmd = ["/sbin/useradd",
                       "-c", user["real_name"],
                       "-m",
                       "-G", "users",
                       "-p", user["password"],
                       user["username"]]
        try:
            #subprocess.run(useradd_cmd, check=True)
            print(f"User creation command: {useradd_cmd}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating user {user['username']}: {e}")
        
        writer.writerow(user)
