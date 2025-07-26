import click
from instrumentation.run_profiler import run_nsys
from processing.kernel_summary import summarize_kernels
from processing.parse_trace import extract_kernel_data
from visualization.plot_kernels import plot_kernel_durations

from processing.parse_trace_instances import parse_kernel_instances
from visualization.plot_timeline import plot_kernel_timeline

@click.group()
def cli():
    """kernalyse - CUDA Kernel Profiler"""
    pass

@cli.command()
def profile():
    """Run profiler and show kernel summary chart"""
    run_nsys()
    df = extract_kernel_data("data/profile")
    plot_kernel_durations(df)

@cli.command()
def timeline():
    df = parse_kernel_instances("data/profile")
    print(df[["name", "start_ms", "duration_ms"]].head())

    summary = summarize_kernels(df)
    print("\nKernel Summary:\n", summary)

    plot_kernel_timeline(df)

if __name__ == "__main__":
    cli()
