import os
import click
from instrumentation.run_profiler import run_nsys
from processing.parse_trace import extract_kernel_data
from visualisation.plot_kernels import plot_kernel_durations

@click.group()
def cli():
    pass

@cli.command()
@click.option('--prompt', required=True, help="Text prompt to send to the model")
@click.option('--model', default="examples/bert/model.onnx", show_default=True, help="Path to ONNX model to use for inference")
@click.option('--trace-output', default="data/profile", show_default=True, help="Prefix path for trace output (without .nsys-rep)")
def profile(prompt, model, trace_output):
    """Profile BERT model with a prompt and visualize kernel usage."""
    print(f"[CLI] Profiling model: {model}")
    print(f"[CLI] Prompt: {prompt}")

    run_nsys(model=model, prompt=prompt, trace_output=trace_output)

    if not os.path.exists(f"{trace_output}.nsys-rep"):
        print(f"[ERROR] No trace file generated: {trace_output}.nsys-rep")
        return

    df = extract_kernel_data(trace_output)
    print(f"[CLI] Extracted {len(df)} kernel records.")
    plot_kernel_durations(df)
    print("[CLI] Saved kernel timeline to data/kernel_plot.html")

if __name__ == "__main__":
    cli()
