import sys
import onnxruntime as ort
from transformers import BertTokenizer
import numpy as np

if len(sys.argv) < 3:
    print("Usage: run_onnx.py <model_path> <prompt>")
    sys.exit(1)

model_path = sys.argv[1]
text = sys.argv[2]

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
session = ort.InferenceSession(model_path, providers=["CUDAExecutionProvider"])

inputs = tokenizer(text, return_tensors="np", padding="max_length", truncation=True, max_length=128)

onnx_inputs = {
    "input_ids": inputs["input_ids"],
    "attention_mask": inputs["attention_mask"],
    "token_type_ids": inputs.get("token_type_ids", np.zeros_like(inputs["input_ids"]))
}

print(f"[INFO] Running inference on: {text}")
outputs = session.run(None, onnx_inputs)
print(f"[INFO] Output shape: {outputs[0].shape}")
