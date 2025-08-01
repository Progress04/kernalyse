import plotly.express as px
import pandas as pd

def plot_kernel_durations(df, out_file="data/kernel_plot.html"):
    df_sorted = df.sort_values("duration_ms", ascending=False).copy()

    fig = px.bar(
        df_sorted,
        x="duration_ms",
        y="name",
        orientation="h",
        labels={"duration_ms": "Duration (ms)", "name": "Kernel"},
        title="CUDA Kernel Execution Times",
    )

    fig.update_layout(height=600, yaxis=dict(autorange="reversed"))
    fig.write_html(out_file)
    print(f"[INFO] Interactive plot saved to: {out_file}")
