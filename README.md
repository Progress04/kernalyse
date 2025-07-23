# kernalyse

A profiler & visualizer for LLM kernels.

## Overview

`kernalyse` is a tool designed to profile and visualize CUDA kernel execution for large language model (LLM) workloads. It provides a layered architecture to instrument, process, store, and visualize kernel execution data, enabling developers to analyze and optimize their GPU workloads.

## Features

- **Instrumentation Layer**: Hooks into CUDA and Triton kernels to collect execution traces.
- **Processing Layer**: Parses trace data and analyzes kernel performance.
- **Storage Layer**: Stores metrics and artifacts in SQLite or Parquet formats.
- **Visualization Layer**: Generates visual reports using a web UI or CLI tools.
- **User Interface**: Command-line tools and APIs for seamless integration.

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

4. **Visualization Layer**:
   - `Web UI (React + D3)`
   - `CLI Report Generator`

5. **User Interface**:
   - `Command-line Tool (kernalyse)`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/kernalyse.git
   cd kernalyse
   ```
2. Install dependencies:
   - NVIDIA Nsight Systems (`nsys`)
   - CUDA Toolkit
   - Python 3.8+ with `pandas` and `matplotlib`

## Usage

### Profiling a CUDA Application

1. Compile your CUDA application (e.g., `vector_add.cu`):
   ```bash
   nvcc -o examples/vector_add examples/vector_add.cu
   ```

2. Run the profiler:
   ```bash
   python -m interface.cli.main profile
   ```

3. View the kernel execution times in a bar chart.

### Example Output

- **CLI Output**:

Running: nsys profile -t cuda -o data/profile --force-overwrite true ./examples/vector_add


- **Visualization**:
A bar chart showing kernel execution times.

## Code Structure

- **`instrumentation/`**: Contains tools for profiling CUDA applications.
- `run_profiler.py`: Runs NVIDIA Nsight Systems to collect kernel traces.

- **`processing/`**: Handles trace parsing and kernel analysis.
- `parse_trace.py`: Extracts kernel execution data from `.nsys-rep` files.

- **`visualization/`**: Generates visual reports.
- `plot_kernels.py`: Plots kernel execution times using Matplotlib.

- **`examples/`**: Example CUDA applications.
- `vector_add.cu`: A simple vector addition kernel.

- **`interface/`**: CLI tools for interacting with the system.
- `cli/main.py`: Entry point for the command-line interface.
