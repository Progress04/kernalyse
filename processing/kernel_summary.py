def summarize_kernels(df):
    summary = (
        df.groupby("name")["duration_ms"]
        .agg(["count", "sum", "mean", "min", "max"])
        .rename(columns={
            "count": "invocations",
            "sum": "total_time_ms",
            "mean": "avg_time_ms",
            "min": "min_time_ms",
            "max": "max_time_ms"
        })
        .sort_values("total_time_ms", ascending=False)
    )
    return summary
