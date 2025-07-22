import matplotlib.pyplot as plt

def plot_kernel_durations(df):
    df_sorted = df.sort_values("duration_ms", ascending=False)
    plt.figure(figsize=(10, 4))
    plt.bar(df_sorted["name"], df_sorted["duration_ms"])
    plt.ylabel("Duration (ms)")
    plt.title("CUDA Kernel Execution Time")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()
