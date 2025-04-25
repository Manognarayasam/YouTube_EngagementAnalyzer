# scripts/clean_comments.py
import pandas as pd
import nltk
import re
from nltk.corpus import stopwords

nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = re.sub(r"http\S+|[^a-zA-Z\s]", "", text)
    words = text.lower().split()
    return " ".join([w for w in words if w not in stop_words])

# df = pd.read_csv("data/raw_comments.csv")
# df["clean_text"] = df["text"].apply(clean_text)
# df.to_csv("data/cleaned_comments.csv", index=False)
# print("Cleaned comments saved to data/cleaned_comments.csv")
