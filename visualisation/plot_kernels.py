import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

def plot_kernel_durations(df: pd.DataFrame, out_file: str = "data/kernel_plot.html", top_n: int = 20):
    if "duration_ms" not in df or "name" not in df:
        print("[ERROR] DataFrame missing required columns.")
        return

    df = df.copy()
    df = df.sort_values("duration_ms", ascending=False).head(top_n)

    # Minimal labels: kernel_01, kernel_02, ...
    df["label"] = [f"kernel_{i+1:02d}" for i in range(len(df))]

    fig = go.Figure(
        data=[
            go.Bar(
                x=df["duration_ms"],
                y=df["label"],
                orientation="h",
                marker=dict(color="rgba(99,102,241,0.8)", line=dict(color="rgba(99,102,241,1.0)", width=1)),
                hovertext=df["name"],
                hoverinfo="text+x"
            )
        ]
    )

    fig.update_layout(
        title="Top CUDA Kernel Execution Times",
        xaxis_title="Duration (ms)",
        yaxis_title="Kernel",
        yaxis=dict(autorange="reversed"),
        height=600,
        margin=dict(l=100, r=40, t=60, b=40),
        font=dict(family="Inter, sans-serif", size=14)
    )

    fig.write_html(out_file)
    print(f"[INFO] Saved interactive plot to {out_file}")

def plot_kernel_timeline(df: pd.DataFrame, out_file="data/kernel_timeline.html", top_n=100):
    if df.empty or not {"name", "start_ms", "end_ms", "duration_ms"}.issubset(df.columns):
        print("[ERROR] DataFrame missing required columns or is empty.")
        return

    df = df.copy().sort_values("start_ms").head(top_n)

    # Make time relative to first kernel
    first_start = df["start_ms"].min()
    df["start"] = df["start_ms"] - first_start
    df["duration"] = df["end_ms"] - df["start_ms"]
    df["label"] = [f"kernel_{i+1:03d}" for i in range(len(df))]

    fig = go.Figure()

    for _, row in df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["duration"]],
            y=[row["label"]],
            base=row["start"],
            orientation='h',
            hovertext=(
                f"{row['name']}<br>"
                f"Start: {row['start']:.3f} ms<br>"
                f"Duration: {row['duration']:.3f} ms"
            ),
            hoverinfo="text",
            marker=dict(color="rgba(56, 161, 105, 0.7)", line=dict(color="rgba(56, 161, 105, 1.0)", width=1)),
            showlegend=False
        ))

    fig.update_layout(
        title="CUDA Kernel Execution Timeline (Relative)",
        xaxis_title="Time since first kernel (ms)",
        yaxis_title="Kernel",
        barmode='stack',
        height=min(40 * len(df), 1000),
        margin=dict(l=200, r=40, t=40, b=40),
    )

    fig.write_html(out_file)
    print(f"[INFO] Saved interactive Gantt chart to {out_file}")