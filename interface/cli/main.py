import os
import subprocess
import click
from instrumentation.run_profiler import run_nsys
from processing.kernel_summary import extract_kernel_data
from processing.kernel_data import extract_kernel_events
from visualisation.plot_kernels import plot_kernel_durations, plot_kernel_timeline

@click.group()
def cli():
    pass

@cli.command()
@click.option('--prompt', help="Text prompt to send to the model (required if using --model)")
@click.option('--model', help="Path to ONNX model for LLM inference")
@click.option('--binary', help="Path to compiled CUDA binary to profile (e.g., examples/vector_add)")
@click.option('--trace-output', default="data/profile", show_default=True, help="Prefix path for trace output")
def profile(prompt, model, binary, trace_output):
    """
    Profile either an ONNX model with a prompt, or a compiled CUDA kernel binary.
    """
    if (model and binary) or (not model and not binary):
        print("[ERROR] You must specify either --model or --binary (but not both).")
        return

    if model:
        if not prompt:
            print("[ERROR] --prompt is required when using --model.")
            return
        print(f"[CLI] Profiling ONNX model: {model}")
        print(f"[CLI] Prompt: {prompt}")
        try:
            run_nsys(model=model, prompt=prompt, trace_output=trace_output)
        except subprocess.CalledProcessError as e:
            print("[ERROR] Failed to run nsys on model inference:")
            print(e)
            return

    elif binary:
        print(f"[CLI] Profiling CUDA binary: {binary}")
        try:
            run_nsys(binary=binary, trace_output=trace_output)
        except subprocess.CalledProcessError as e:
            print("[ERROR] Failed to run nsys on binary:")
            print(e)
            return

    if not os.path.exists(f"{trace_output}.nsys-rep"):
        print(f"[ERROR] No trace file generated: {trace_output}.nsys-rep")
        return

    df_kernel_summary = extract_kernel_data(trace_output)
    print(f"[CLI] Extracted {len(df_kernel_summary)} kernel records.")
    print("[DEBUG] Columns:", df_kernel_summary.columns.tolist())
    print("[DEBUG] Head:\n", df_kernel_summary.head())
    plot_kernel_durations(df_kernel_summary)

    df_kernel_events = extract_kernel_events(trace_output)
    print(f"[CLI] Extracted {len(df_kernel_events)} kernel events.")
    print("[DEBUG] Columns:", df_kernel_events.columns.tolist())
    print("[DEBUG] Head:\n", df_kernel_events.head())
    plot_kernel_timeline(df_kernel_events)
    print("[CLI] Saved kernel timeline to data/kernel_plot.html")

if __name__ == "__main__":
    cli()
