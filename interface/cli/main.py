import click
from instrumentation.run_profiler import run_nsys
from processing.parse_trace import extract_kernel_data
from visualization.plot_kernels import plot_kernel_durations

@click.command()
def profile():
    run_nsys()
    df = extract_kernel_data("data/profile")
    plot_kernel_durations(df)

if __name__ == "__main__":
    profile()
