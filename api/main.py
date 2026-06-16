import os
from typing import List
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.quantize import apply_dynamic_quantization

app = FastAPI(title="NLP Text Classifier API", version="1.0.0")

MODEL_DIR = os.getenv("MODEL_DIR", "models/sentiment-bert-lora")
USE_QUANTIZATION = os.getenv("USE_QUANTIZATION", "true").lower() == "true"

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
model.eval()

if USE_QUANTIZATION:
    model = apply_dynamic_quantization(model)

ID2LABEL = model.config.id2label


class PredictionRequest(BaseModel):
    texts: List[str]


class PredictionItem(BaseModel):
    text: str
    label: str
    confidence: float


class PredictionResponse(BaseModel):
    predictions: List[PredictionItem]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    inputs = tokenizer(
        request.texts, truncation=True, padding=True, max_length=64, return_tensors="pt"
    )
    with torch.no_grad():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=-1)
        confidences, predicted_ids = torch.max(probabilities, dim=-1)

    results = [
        PredictionItem(
            text=text,
            label=ID2LABEL[predicted_id.item()],
            confidence=confidence.item(),
        )
        for text, predicted_id, confidence in zip(request.texts, predicted_ids, confidences)
    ]

    return PredictionResponse(predictions=results)
