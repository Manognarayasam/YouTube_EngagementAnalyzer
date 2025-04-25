import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load cleaned comments
df = pd.read_csv("data/cleaned_comments.csv")

# Handle missing or non-string values
df = df.dropna(subset=["clean_text"])
df = df[df["clean_text"].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0)]

# Sentiment score function
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Apply sentiment scoring
df["sentiment_score"] = df["clean_text"].apply(get_sentiment)

# Labeling function
def label_sentiment(score):
    if score > 0.1:
        return "positive"
    elif score < -0.1:
        return "negative"
    else:
        return "neutral"

# Apply labeling
df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)

# Save the labeled data
df.to_csv("data/sentiment_labeled_comments.csv", index=False)
print("✅ Sentiment-labeled comments saved to data/sentiment_labeled_comments.csv")

# Visualize sentiment distribution
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x="sentiment_label", order=["positive", "neutral", "negative"])
plt.title("Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Comments")
plt.tight_layout()
plt.show()

# Summary breakdown
summary = df["sentiment_label"].value_counts(normalize=True) * 100
print("\n📊 Sentiment Breakdown (%):")
print(summary.round(2))

def generate_wordcloud(text, title):
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(text))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    plt.show()

# Generate word clouds per sentiment
for label in ["positive", "neutral", "negative"]:
    texts = df[df["sentiment_label"] == label]["clean_text"]
    generate_wordcloud(texts, f"Word Cloud - {label.capitalize()} Comments")