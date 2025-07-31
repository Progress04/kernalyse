FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /workspace

# System dependencies
RUN apt-get update && apt-get install -y \
    wget curl git python3 python3-pip python3-dev \
    libglib2.0-0 libsm6 libxrender1 libxext6 \
    build-essential unzip && \
    apt-get clean

# Python packages
RUN pip3 install --upgrade pip && \
    pip3 install \
    onnx onnxruntime-gpu \
    pandas matplotlib plotly click transformers

# Install Nsight Systems CLI from NVIDIA (scripted)
RUN apt-get update && apt-get install -y cuda-nsight-systems-12-2

CMD ["/bin/bash"]
