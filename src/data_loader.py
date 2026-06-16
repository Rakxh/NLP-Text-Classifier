import os
import pandas as pd
from sklearn.model_selection import train_test_split

LABEL_MAP = {"negative": 0, "neutral": 1, "positive": 2}


def load_data(source_path="data/sentiment_dataset.csv", output_dir="data"):
    df = pd.read_csv(source_path)
    df["label_id"] = df["label"].map(LABEL_MAP)
    os.makedirs(output_dir, exist_ok=True)
    train_df, test_df = train_test_split(
        df, test_size=0.2, random_state=42, stratify=df["label_id"]
    )
    train_df.to_csv(os.path.join(output_dir, "train.csv"), index=False)
    test_df.to_csv(os.path.join(output_dir, "test.csv"), index=False)
    return train_df, test_df


if __name__ == "__main__":
    load_data()
