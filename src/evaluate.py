import os
import json
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import classification_report

LABEL_MAP = {"negative": 0, "neutral": 1, "positive": 2}


def evaluate_model(
    model_dir=os.getenv("MODEL_DIR", "models/sentiment-bert-lora"),
    test_path="data/test.csv",
    output_path="metrics.json",
    batch_size=32,
):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)
    model = AutoModelForSequenceClassification.from_pretrained(model_dir)
    model.eval()

    test_df = pd.read_csv(test_path)
    texts = test_df["text"].tolist()
    labels = test_df["label_id"].tolist()

    predictions = []
    with torch.no_grad():
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            inputs = tokenizer(
                batch, truncation=True, padding=True, max_length=64, return_tensors="pt"
            )
            logits = model(**inputs).logits
            predictions.extend(logits.argmax(dim=-1).tolist())

    report = classification_report(
        labels, predictions, target_names=list(LABEL_MAP.keys()), output_dict=True
    )

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return report


if __name__ == "__main__":
    evaluate_model()
