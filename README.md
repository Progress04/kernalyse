# Kernalyse

A profiler & visualiser for LLM kernels.

## Overview

`kernalyse` is a tool designed to profile and visualise CUDA kernel execution for large language model (LLM) workloads. It provides a layered architecture to instrument, process, store, and visualise kernel execution data, enabling developers to analyze and optimize their GPU workloads.

## Features

- **Instrumentation Layer**: Hooks into CUDA and Triton kernels to collect execution traces.
- **Processing Layer**: Parses trace data and analyzes kernel performance.
- **Storage Layer**: Stores metrics and artifacts in SQLite or Parquet formats.
- **Visualisation Layer**: Generates visual reports using a web UI or CLI tools.
- **User Interface**: Command-line tools and Flask-based Web UI for seamless integration.

## System Architecture

The system architecture is organized into five layers:

1. **Instrumentation Layer**:
   - `CUDA Profiler`
   - `Script Runner (CLI)`

2. **Processing Layer**:
   - `Trace Parser`
   - `Kernel Analyzer`
   - `Model-Aware Mapper`

3. **Storage Layer**:
   - `Metrics DB (SQLite / Parquet)`
   - `Trace Artifact Store`

4. **Visualisation Layer**:
   - `Web UI (Flask + Plotly)`
   - `CLI Report Generator`

5. **User Interface**:
   - `Command-line Tool (kernalyse)`
   - `Flask App`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kernalyse.git
   cd kernalyse
   ```

2. Install dependencies:
   - NVIDIA Nsight Systems (`nsys`)
   - CUDA Toolkit
   - Python 3.8+ with the following packages:
     ```bash
     pip install -r requirements.txt
     ```

3. Download the ONNX BERT model:
   ```bash
   python3 -m transformers.onnx --model=bert-base-cased --feature=sequence-classification onnx-models/bert
   ```

## Usage

###  Building the Docker Image

To ensure a consistent environment with the correct CUDA, Nsight Systems (`nsys`), and Python setup, build the Docker image using:

```bash
docker build -t kernalyse-nsys .
```

### Run via CLI

To profile the default BERT ONNX model using a custom prompt:
```bash
python -m interface.cli.main profile --prompt "Your input text here"
```

### Run via Flask Web UI

To launch the web app:
```bash
./run.sh
```

This will:
- Launch a Flask server on http://localhost:5000
- Let you enter text input
- Profile CUDA kernels for the BERT model
- Display interactive kernel timeline plots

### Profiling Other CUDA Apps

Example for a custom CUDA binary:

1. Compile:
   ```bash
   nvcc -o examples/vector_add examples/vector_add.cu
   ```

2. Profile it:
   ```bash
   python -m interface.cli.main profile --target examples/vector_add
   ```

## Code Structure

- **`instrumentation/`**: Tools for profiling.
  - `run_profiler.py`: Runs Nsight Systems (`nsys`).

- **`processing/`**: Extract and parse kernel traces.
  - `parse_trace.py`: Converts `.nsys-rep` to tabular format.

- **`visualisation/`**: Generate plots.
  - `plot_kernels.py`: Timeline visualization using Plotly.

- **`interface/`**: CLI interface.
  - `cli/main.py`: Main CLI logic.

- **`app/`**: Flask web interface.
  - `app.py`: Launches the server.

- **`examples/`**: Profiling targets.
  - `inference_runners/run_onnx.py`: Executes the ONNX BERT model.

- **`data/`**: Stores trace files and plots.
  - `profile.nsys-rep`, `kernel_plot.html`, etc.

## License

This project is licensed under the terms of the NVIDIA Deep Learning Container License.