import csv
import random

random.seed(42)

products = [
    "laptop", "smartphone", "headphones", "blender", "vacuum cleaner",
    "coffee maker", "office chair", "running shoes", "backpack", "smartwatch",
    "wireless mouse", "monitor", "keyboard", "speaker", "tablet",
    "air purifier", "electric kettle", "fitness tracker", "camera", "router",
]

positive_templates = [
    "The {product} exceeded my expectations and works flawlessly.",
    "I am extremely happy with this {product}, it performs great.",
    "This {product} is fantastic, well built and reliable.",
    "Absolutely love the {product}, best purchase this year.",
    "The {product} arrived quickly and works perfectly every time.",
    "Great value for money, the {product} is excellent quality.",
    "The {product} has amazing battery life and feels premium.",
    "Highly recommend this {product}, it solved all my needs.",
    "The {product} is sturdy, fast, and easy to use.",
    "I'm impressed by how well the {product} performs daily.",
]

negative_templates = [
    "The {product} stopped working after just a few days.",
    "I am disappointed with this {product}, it feels cheap.",
    "This {product} broke quickly and customer service was unhelpful.",
    "Terrible experience, the {product} never worked properly.",
    "The {product} arrived damaged and was hard to return.",
    "Poor build quality, the {product} is not worth the price.",
    "The {product} is slow, unreliable, and frustrating to use.",
    "I regret buying this {product}, it failed within a week.",
    "The {product} overheats constantly and the battery drains fast.",
    "Customer support ignored my complaints about the faulty {product}.",
]

neutral_templates = [
    "The {product} is okay, nothing particularly special about it.",
    "The {product} works as described, average performance overall.",
    "It does the job, but the {product} is not very impressive.",
    "The {product} is fine for basic use, nothing more.",
    "I have mixed feelings about the {product}, some good some bad.",
    "The {product} meets basic expectations but lacks extra features.",
    "Decent {product} for the price, though not outstanding.",
    "The {product} is functional but feels a bit outdated.",
    "Average quality {product}, does what it says.",
    "The {product} is acceptable, though I expected slightly more.",
]


def generate_rows(n_per_class=200):
    rows = []
    for _ in range(n_per_class):
        product = random.choice(products)
        template = random.choice(positive_templates)
        rows.append((template.format(product=product), "positive"))

        product = random.choice(products)
        template = random.choice(negative_templates)
        rows.append((template.format(product=product), "negative"))

        product = random.choice(products)
        template = random.choice(neutral_templates)
        rows.append((template.format(product=product), "neutral"))

    random.shuffle(rows)
    return rows


def save_dataset(output_path="data/sentiment_dataset.csv", n_per_class=200):
    rows = generate_rows(n_per_class)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)


if __name__ == "__main__":
    save_dataset()
