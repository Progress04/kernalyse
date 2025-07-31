import subprocess
import os
import sys
from instrumentation.model_registry import MODEL_REGISTRY

def run_nsys(target: str):
    if target not in MODEL_REGISTRY:
        raise ValueError(f"Unknown target: {target}")

    info = MODEL_REGISTRY[target]
    output_path = "data/profile"
    os.makedirs("data", exist_ok=True)

    if info["type"] == "onnx":
        cmd = [
            "nsys", "profile", "-t", "cuda",
            "-o", output_path,
            "--force-overwrite", "true",
            sys.executable,
            "examples/inference_runners/run_onnx.py",
            info["model_path"]
        ]
    elif info["type"] == "binary":
        cmd = [
            "nsys", "profile", "-t", "cuda",
            "-o", output_path,
            "--force-overwrite", "true",
            info["path"]
        ]
    else:
        raise ValueError("Unknown type")

    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)
