import subprocess

def run_nsys(model=None, prompt=None, binary=None, trace_output="data/profile"):
    print(f"[CLI] Profiling CUDA binary once again!: {binary}")
    if binary:
        cmd = [
            "nsys", "profile",
            "-t", "cuda",
            "-o", trace_output,
            "--force-overwrite", "true",
            binary
        ]

    elif model and prompt:
        cmd = [
        "nsys", "profile",
        "-t", "cuda",
        "-o", trace_output,
        "--stats", "true",
        "--force-overwrite", "true",
        "python3", "examples/inference_runners/run_onnx.py", model, prompt
        ]
    else:
        raise ValueError("Must provide either `binary` or both `model` and `prompt`.")

    print("[Profiler] Running command:")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
