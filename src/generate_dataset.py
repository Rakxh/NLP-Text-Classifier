import csv
import random

random.seed(42)

products = [
    "laptop", "smartphone", "headphones", "blender", "vacuum cleaner",
    "coffee maker", "office chair", "running shoes", "backpack", "smartwatch",
    "wireless mouse", "monitor", "keyboard", "speaker", "tablet",
    "air purifier", "electric kettle", "fitness tracker", "camera", "router",
]

# ── POSITIVE ──────────────────────────────────────────────────────────────────
positive_templates = [
    # formal / long
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
    "Five stars for this {product}, could not be happier.",
    "The {product} is exactly what I was looking for.",
    "Outstanding {product}, exceeded all my expectations.",
    "Best {product} I have ever owned, truly impressive.",
    "The {product} is worth every penny, highly satisfied.",
    # casual / short
    "Love this {product}!",
    "Great {product}, really happy with it.",
    "Amazing {product}, 10/10 would buy again.",
    "This {product} is so good.",
    "Wow, the {product} blew me away.",
    "Super happy with my new {product}.",
    "The {product} is awesome!",
    "Good one, really glad I bought this {product}.",
    "Best buy ever — the {product} is perfect.",
    "Totally worth it, love the {product}.",
    "The {product} works like a charm.",
    "Solid {product}, no complaints.",
    "Really good {product}, does exactly what I need.",
    "Happy with this {product}, works well.",
    "Great stuff, the {product} is top notch.",
    # very short
    "Great product.",
    "Love it!",
    "Highly recommend.",
    "Amazing quality.",
    "Works perfectly.",
    "Worth every penny.",
    "Very satisfied.",
    "Excellent purchase.",
    "Good one.",
    "Really good.",
    "So happy with this.",
    "Fantastic!",
    "10 out of 10.",
    "Best purchase.",
    "Absolutely love it.",
]

# ── NEGATIVE ──────────────────────────────────────────────────────────────────
negative_templates = [
    # formal / long
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
    "Worst {product} I have ever bought, completely useless.",
    "The {product} broke down after the first use.",
    "Extremely disappointed with this {product}.",
    "The {product} is a complete waste of money.",
    "Do not buy this {product}, it is terrible quality.",
    # casual / short
    "Terrible {product}, do not buy.",
    "Such a bad {product}, wasted my money.",
    "The {product} is rubbish.",
    "Hate this {product}, it keeps breaking.",
    "Awful {product}, would not recommend.",
    "The {product} is garbage.",
    "Really bad {product}, very disappointed.",
    "Not happy at all with the {product}.",
    "The {product} sucks, total waste.",
    "Broken {product}, very frustrating.",
    "This {product} is a scam.",
    "Regret buying this {product}.",
    "The {product} stopped working immediately.",
    "Bad experience with the {product}.",
    "Cheap and useless {product}.",
    # very short
    "Terrible product.",
    "Waste of money.",
    "Do not buy.",
    "Very disappointed.",
    "Broken on arrival.",
    "Awful quality.",
    "Total garbage.",
    "Not worth it.",
    "Really bad.",
    "Hate it.",
    "Worst purchase ever.",
    "Completely useless.",
    "So frustrated.",
    "Regret this purchase.",
    "Absolutely terrible.",
]

# ── NEUTRAL ───────────────────────────────────────────────────────────────────
neutral_templates = [
    # formal / long
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
    "The {product} is neither great nor terrible, just average.",
    "Mixed results with the {product}, some things work well others do not.",
    "The {product} is passable but I would not buy it again.",
    "It is an okay {product}, nothing to write home about.",
    "The {product} gets the job done but there is room for improvement.",
    # casual / short
    "It is okay I guess.",
    "The {product} is alright, nothing special.",
    "Meh, the {product} is just average.",
    "Not bad, not great either.",
    "The {product} is decent enough.",
    "It works, but nothing impressive about the {product}.",
    "Kind of mixed on this {product}.",
    "Average {product}, does its job.",
    "The {product} is fine I suppose.",
    "It is what it is, just an okay {product}.",
    "Not amazing but not bad either.",
    "The {product} is passable.",
    "Pretty average product.",
    "It does what it should, nothing more.",
    "Could be better, could be worse.",
    # very short
    "It is okay.",
    "Average product.",
    "Nothing special.",
    "Decent enough.",
    "Just okay.",
    "Not bad.",
    "Meh.",
    "It is alright.",
    "So so.",
    "Could be better.",
    "Neither good nor bad.",
    "Does the job.",
    "Fine I guess.",
    "Mixed feelings.",
    "Middle of the road.",
]


def generate_rows(n_per_class=300):
    rows = []

    for template in positive_templates:
        product = random.choice(products)
        rows.append((template.format(product=product), "positive"))

    for template in negative_templates:
        product = random.choice(products)
        rows.append((template.format(product=product), "negative"))

    for template in neutral_templates:
        product = random.choice(products)
        rows.append((template.format(product=product), "neutral"))

    # fill remaining with random product-template combos to hit n_per_class
    current_counts = {"positive": len(positive_templates),
                      "negative": len(negative_templates),
                      "neutral": len(neutral_templates)}

    for label, templates in [("positive", positive_templates),
                              ("negative", negative_templates),
                              ("neutral", neutral_templates)]:
        needed = n_per_class - current_counts[label]
        for _ in range(needed):
            product = random.choice(products)
            template = random.choice(templates)
            rows.append((template.format(product=product), label))

    random.shuffle(rows)
    return rows


def save_dataset(output_path="data/sentiment_dataset.csv", n_per_class=300):
    rows = generate_rows(n_per_class)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["text", "label"])
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows ({len(rows)//3} per class)")


if __name__ == "__main__":
    save_dataset()