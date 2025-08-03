from flask import Flask, request, render_template
import subprocess
import os
import logging

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PLOT_PATH = os.path.join(BASE_DIR, "data", "kernel_plot.html")
PROJECT_VOLUME = BASE_DIR
CONTAINER_WORKDIR = "/workspace"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form.get("user_input", "Hello BERT")

        container_cmd = [
            "docker", "run", "--rm",
            "--runtime=nvidia",
            "-v", f"{PROJECT_VOLUME}:{CONTAINER_WORKDIR}",
            "-w", CONTAINER_WORKDIR,
            "kernalyse-nsys",
            "bash", "-c",
            f"python3 -m interface.cli.main profile "
            f"--prompt \"{user_input}\" "
            f"--model examples/bert/model.onnx "
            f"--trace-output data/profile"
        ]

        print("Running Docker command:")
        print(" ".join(container_cmd))

        try:
            result = subprocess.run(container_cmd, check=True, capture_output=True, text=True)
            print("---- STDOUT ----")
            print(result.stdout)
            print("---- STDERR ----")
            print(result.stderr)
        except subprocess.CalledProcessError as e:
            return f"<h3>🚨 Error during profiling</h3><pre>{e}</pre>"

        if not os.path.exists(PLOT_PATH):
            return "<h3>❌ No plot was generated</h3>"

    return render_template("index.html", plot_exists=os.path.exists(PLOT_PATH))

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
