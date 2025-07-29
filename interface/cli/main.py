import click
from instrumentation.run_profiler import run_nsys
from processing.parse_trace import extract_kernel_data
from visualization.plot_kernels import plot_kernel_durations

@click.group()
def cli():
    pass

@cli.command()
@click.option('--target', default='multi_kernel_ops', help='Name of target executable to profile.')
def profile(target):
    run_nsys(target)
    df = extract_kernel_data("data/profile")
    plot_kernel_durations(df)

if __name__ == "__main__":
    cli()
