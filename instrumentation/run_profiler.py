import subprocess

def run_nsys(model, prompt, trace_output):
    """Runs inference on the given model with prompt and profiles it using nsys."""
    cmd = [
        "nsys", "profile",
        "-t", "cuda",
        "-o", trace_output,
        "--force-overwrite", "true",
        "python3", "examples/inference_runners/run_onnx.py", model, prompt
    ]
    print(f"[nsys] Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
