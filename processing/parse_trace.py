import subprocess
import pandas as pd
import re

def extract_kernel_data(trace_file: str) -> pd.DataFrame:
    trace_path = trace_file if trace_file.endswith(".nsys-rep") else trace_file + ".nsys-rep"

    result = subprocess.run(
        ["nsys", "stats", "--report", "cuda_gpu_kern_sum", "--force-export=true", trace_path],
        check=True,
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()
    kernel_lines = []
    capture = False
    skip_next = False

    for line in lines:
        if line.strip().startswith("Time (%)") and "Name" in line:
            capture = True
            skip_next = True  # skip the "------" underline
            continue
        if skip_next:
            skip_next = False
            continue
        if capture and line.strip() == "":
            break   # blank line means end of table
        if capture:
            kernel_lines.append(line.strip())

    records = []
    for line in kernel_lines:
        parts = re.split(r"\s{2,}", line)
        try:
            if len(parts) >= 9:
                name = parts[8]
                duration_ns = int(parts[1].replace(",", ""))
                records.append((name, duration_ns))
        except ValueError:
            print(f"[WARN] Skipping invalid row: {line}")
            continue

    df = pd.DataFrame(records, columns=["name", "duration_ns"])
    df["duration_ms"] = df["duration_ns"] / 1e6
    return df
