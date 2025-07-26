import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import seaborn as sns

def plot_kernel_timeline(df):
    # Assign a numeric y-position per kernel instance grouped by name
    df = df.copy()
    df["y"] = df.groupby("name").cumcount()

    # Get distinct colors for each kernel name
    unique_kernels = df["name"].unique()
    palette = sns.color_palette("husl", len(unique_kernels))
    color_map = dict(zip(unique_kernels, palette))

    fig, ax = plt.subplots(figsize=(12, 6))

    for _, row in df.iterrows():
        ax.broken_barh(
            [(row["start_ms"], row["duration_ms"])],
            (row["y"] - 0.4, 0.8),
            facecolors=color_map[row["name"]],
            edgecolors="black",
            linewidth=0.3
        )

    ax.set_xlabel("Time (ms)")
    ax.set_ylabel("Kernel Instance")
    ax.set_title("Grouped CUDA Kernel Timeline")
    ax.grid(True, axis="x", linestyle="--", alpha=0.5)

    # Legend
    patches = [mpatches.Patch(color=color_map[k], label=k) for k in unique_kernels]
    ax.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    plt.show()
