import sqlite3
import pandas as pd

def extract_kernel_events(trace_file: str, limit: int = 1000) -> pd.DataFrame:
    trace_path = trace_file if trace_file.endswith(".sqlite") else trace_file + ".sqlite"
    conn = sqlite3.connect(trace_path)
    query = """
    SELECT
        demangledName AS name,
        start AS start_ns,
        end AS end_ns
    FROM CUPTI_ACTIVITY_KIND_KERNEL
    ORDER BY start_ns
    LIMIT ?
    """

    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()

    # Convert to milliseconds
    df["start_ms"] = df["start_ns"] / 1e6
    df["end_ms"] = df["end_ns"] / 1e6
    df["duration_ms"] = df["end_ms"] - df["start_ms"]

    return df[["name", "start_ms", "end_ms", "duration_ms"]]
