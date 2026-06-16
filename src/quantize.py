import os
import time
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def apply_dynamic_quantization(model):
    return torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)


def benchmark_latency(model, tokenizer, texts, batch_size=8, runs=20):
    inputs = tokenizer(
        texts[:batch_size], truncation=True, padding=True, max_length=64, return_tensors="pt"
    )
    model.eval()
    with torch.no_grad():
        for _ in range(3):
            model(**inputs)
        start = time.time()
        for _ in range(runs):
            model(**inputs)
        end = time.time()
    return (end - start) / runs


def run_benchmark(model_dir=os.getenv("MODEL_DIR", "models/sentiment-bert-lora")):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)

    sample_texts = [
        "The product works great and exceeded expectations.",
        "This item broke after a few days, very disappointing.",
        "It is okay, nothing special about it.",
        "Customer support was unhelpful and slow to respond.",
        "The build quality is excellent and battery life is amazing.",
        "I regret this purchase, it stopped working within a week.",
        "Average performance, does what it says on the box.",
        "Fast shipping and the item works perfectly every time.",
    ]

    baseline_latency = benchmark_latency(model, tokenizer, sample_texts)
    quantized_model = apply_dynamic_quantization(model)
    quantized_latency = benchmark_latency(quantized_model, tokenizer, sample_texts)

    improvement = (baseline_latency - quantized_latency) / baseline_latency * 100

    print(f"Baseline latency: {baseline_latency * 1000:.2f} ms")
    print(f"Quantized latency: {quantized_latency * 1000:.2f} ms")
    print(f"Latency improvement: {improvement:.2f}%")

    return baseline_latency, quantized_latency, improvement


if __name__ == "__main__":
    run_benchmark()
