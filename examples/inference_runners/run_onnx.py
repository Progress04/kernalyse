import onnxruntime as ort
import numpy as np
import sys

def run(model_path):
    print(f"[INFO] Loading model: {model_path}")
    print("[INFO] Available providers:", ort.get_available_providers())

    session = ort.InferenceSession(model_path, providers=["CUDAExecutionProvider"])
    print("[INFO] Using provider:", session.get_providers())

    # Dummy input for BERT-like model
    inputs = {
        "input_ids": np.ones((1, 16), dtype=np.int64),
        "attention_mask": np.ones((1, 16), dtype=np.int64),
    }
    
    inputs["token_type_ids"] = np.zeros_like(inputs["input_ids"])

    print("[INFO] Running inference...")
    outputs = session.run(None, inputs)
    print("[INFO] Output shape:", outputs[0].shape)

if __name__ == "__main__":
    run(sys.argv[1])
