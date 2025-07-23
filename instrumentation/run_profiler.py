import subprocess
import os

def run_nsys(target="./examples/vector_add", output="data/profile"):
    os.makedirs("data", exist_ok=True)
    cmd = [
        "nsys", "profile",
        "-t", "cuda",
        "-o", output,
        "--force-overwrite","true",
        target
    ]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
