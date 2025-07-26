# processing/parse_trace_instances.py

import subprocess
import pandas as pd
import re

def parse_kernel_instances(trace_file: str) -> pd.DataFrame:
    trace_path = trace_file if trace_file.endswith(".nsys-rep") else trace_file + ".nsys-rep"

    result = subprocess.run(
        ["nsys", "stats", "--report", "cuda_gpu_trace", "--force-export=true", trace_path],
        check=True,
        capture_output=True,
        text=True
    )

    lines = result.stdout.splitlines()
    kernel_lines = []
    capture = False
    skip_next = False

    for line in lines:
        if line.strip().startswith("Start (ns)") and "Name" in line:
            capture = True
            skip_next = True  # Skip the dashed line
            continue
        if skip_next:
            skip_next = False
            continue
        if capture and line.strip() == "":
            break
        if capture:
            kernel_lines.append(line.strip())

    records = []
    for line in kernel_lines:
        parts = re.split(r"\s{2,}", line)
        try:
            if len(parts) >= 6:
                start_ns = int(parts[0].replace(",", ""))
                duration_ns = int(parts[1].replace(",", ""))
                stream_id = parts[3]
                name = parts[-1]  # Kernel name is usually the last field
                records.append((start_ns, duration_ns, stream_id, name))
        except ValueError:
            continue  # Skip malformed rows

    df = pd.DataFrame(records, columns=["start_ns", "duration_ns", "stream", "name"])
    df["start_ms"] = df["start_ns"] / 1e6
    df["duration_ms"] = df["duration_ns"] / 1e6
    df["end_ms"] = df["start_ms"] + df["duration_ms"]
    return df.sort_values("start_ms")
