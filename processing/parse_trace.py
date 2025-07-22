import subprocess
import pandas as pd

def extract_kernel_data(qdrep_file: str) -> pd.DataFrame:
    csv_file = qdrep_file + "_kernels.csv"

    subprocess.run([
        "nsys", "export",
        "--report", "kernel",
        "--output", csv_file,
        qdrep_file + ".qdrep"
    ], check=True)

    # Parse CSV report
    df = pd.read_csv(csv_file)
    df = df[["Name", "Start (ns)", "Duration (ns)"]]
    df.rename(columns={
        "Name": "name",
        "Start (ns)": "start",
        "Duration (ns)": "duration"
    }, inplace=True)
    df["duration_ms"] = df["duration"] / 1e6
    return df
