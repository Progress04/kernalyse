from flask import Flask, request, render_template
import subprocess
import os
import logging
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model_registry import MODEL_REGISTRY

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PLOT_PATH = os.path.join(BASE_DIR, "data", "kernel_plot.html")
PROJECT_VOLUME = BASE_DIR
CONTAINER_WORKDIR = "/workspace"

@app.route("/", methods=["GET", "POST"])
def index():
    selected_model = None
    user_input = ""
    error = None

    if request.method == "POST":
        selected_model = request.form.get("model_choice")
        user_input = request.form.get("user_input", "")

        model_config = MODEL_REGISTRY.get(selected_model)
        if not model_config:
            return "<h3>❌ Invalid model selected</h3>"

        trace_output = "data/profile"
        if model_config["type"] == "onnx":
            if not user_input.strip():
                return "<h3>❌ Prompt is required for ONNX models</h3>"
            container_cmd = [
                "docker", "run", "--rm",
                "--runtime=nvidia",
                "-v", f"{PROJECT_VOLUME}:{CONTAINER_WORKDIR}",
                "-w", CONTAINER_WORKDIR,
                "kernalyse-nsys",
                "bash", "-c",
                f"python3 -m interface.cli.main profile "
                f"--prompt \"{user_input}\" "
                f"--model {model_config['model_path']} "
                f"--trace-output {trace_output}"
            ]
        elif model_config["type"] == "binary":
            container_cmd = [
                "docker", "run", "--rm",
                "--runtime=nvidia",
                "-v", f"{PROJECT_VOLUME}:{CONTAINER_WORKDIR}",
                "-w", CONTAINER_WORKDIR,
                "kernalyse-nsys",
                "bash", "-c",
                f"python3 -m interface.cli.main profile "
                f"--binary {model_config['path']} "
                f"--trace-output {trace_output}"
            ]
        else:
            return "<h3>❌ Unknown model type</h3>"

        try:
            result = subprocess.run(container_cmd, check=True, capture_output=True, text=True)
            print("---- STDOUT ----\n", result.stdout)
            print("---- STDERR ----\n", result.stderr)
        except subprocess.CalledProcessError as e:
            return f"<h3>🚨 Error during profiling</h3><pre>{e.stderr}</pre>"

    return render_template(
        "index.html",
        model_registry=MODEL_REGISTRY,
        selected_model=selected_model,
        user_input=user_input,
        plot_exists=os.path.exists(PLOT_PATH)
    )

@app.route("/plot")
def show_plot():
    plot_type = request.args.get("type", "bar")
    if plot_type == "gantt":
        path = os.path.join("data", "kernel_timeline.html")
    else:
        path = os.path.join("data", "kernel_plot.html")

    try:
        with open(path, "r") as f:
            return f.read()
    except Exception as e:
        return f"<h3>❌ Failed to load plot</h3><pre>{e}</pre>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
