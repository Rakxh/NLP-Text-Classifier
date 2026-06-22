import os
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding,
)
from peft import LoraConfig, get_peft_model, TaskType
from sklearn.metrics import accuracy_score, f1_score

MODEL_NAME = os.getenv("MODEL_NAME", "bert-base-uncased")
LABEL_MAP = {"negative": 0, "neutral": 1, "positive": 2}
ID2LABEL = {v: k for k, v in LABEL_MAP.items()}


def tokenize_dataset(df, tokenizer, max_length=128):
    dataset = Dataset.from_pandas(
        df[["text", "label_id"]].rename(columns={"label_id": "label"})
    )

    def tokenize_fn(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=max_length)

    return dataset.map(tokenize_fn, batched=True)


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = logits.argmax(axis=-1)
    return {
        "accuracy": accuracy_score(labels, predictions),
        "f1": f1_score(labels, predictions, average="weighted"),
    }


def train_model(
    train_path="data/train.csv",
    test_path="data/test.csv",
    model_dir="models/sentiment-bert-lora",
    epochs=5,
):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    train_dataset = tokenize_dataset(train_df, tokenizer)
    test_dataset = tokenize_dataset(test_df, tokenizer)

    base_model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=len(LABEL_MAP), id2label=ID2LABEL, label2id=LABEL_MAP
    )

    lora_config = LoraConfig(
        task_type=TaskType.SEQ_CLS,
        r=16,
        lora_alpha=32,
        lora_dropout=0.1,
        target_modules=["query", "value"],
    )

    model = get_peft_model(base_model, lora_config)

    training_args = TrainingArguments(
        output_dir="checkpoints",
        num_train_epochs=epochs,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-4,
        eval_strategy="epoch",
        save_strategy="no",
        logging_steps=10,
        report_to=[],
        warmup_ratio=0.1,
    )

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )

    trainer.train()
    metrics = trainer.evaluate()

    merged_model = model.merge_and_unload()

    os.makedirs(model_dir, exist_ok=True)
    merged_model.save_pretrained(model_dir)
    tokenizer.save_pretrained(model_dir)

    print(f"Eval accuracy: {metrics.get('eval_accuracy'):.4f}")
    print(f"Eval F1: {metrics.get('eval_f1'):.4f}")

    return merged_model, metrics


if __name__ == "__main__":
    train_model()