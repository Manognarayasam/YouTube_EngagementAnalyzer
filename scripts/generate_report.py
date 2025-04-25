import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from fpdf import FPDF
import os

def generate_pdf_report(df, output_path="output/sentiment_report.pdf"):
    df["published"] = pd.to_datetime(df["published"])
    df["date"] = df["published"].dt.date
    os.makedirs("output", exist_ok=True)
    # === Sentiment Distribution ===
    plt.figure(figsize=(7, 5))
    sns.countplot(data=df, x="sentiment_label", order=["positive", "neutral", "negative"])
    plt.title("Sentiment Distribution of Comments")
    plt.xlabel("Sentiment")
    plt.ylabel("Number of Comments")
    plt.tight_layout()
    plt.savefig("output/sentiment_distribution.png")
    plt.close()


    # # === Word Clouds ===
    # sentiments = ["positive", "neutral", "negative"]
    # for label in sentiments:
    #     text = " ".join(df[df["sentiment_label"] == label]["clean_text"])
    #     wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    #     plt.figure(figsize=(8, 4))
    #     plt.imshow(wordcloud, interpolation="bilinear")
    #     plt.axis("off")
    #     plt.title(f"{label.capitalize()} Comments")
    #     plt.tight_layout()
    #     plt.savefig(f"output/wordcloud_{label}.png")
    #     plt.close()

            # === Word Clouds ===
    sentiments = ["positive", "neutral", "negative"]
    for label in sentiments:
        texts = df[df["sentiment_label"] == label]["clean_text"]
        texts = texts[texts.str.strip().astype(bool)]  # Remove empty/space-only

        if len(texts) > 0:
            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(" ".join(texts))
            plt.figure(figsize=(8, 4))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            plt.title(f"{label.capitalize()} Comments")
            plt.tight_layout()
            plt.savefig(f"output/wordcloud_{label}.png")
            plt.close()
        else:
            print(f"⚠️ Skipping {label} word cloud — no valid words.")


    # === Sentiment Timeline ===
    timeline = df.groupby("date").agg(
        num_comments=("clean_text", "count"),
        avg_sentiment=("sentiment_score", "mean")
    ).reset_index()
    norm = plt.Normalize(-1, 1)
    colors = plt.cm.RdYlGn(norm(timeline["avg_sentiment"]))
    plt.figure(figsize=(12, 5))
    plt.bar(timeline["date"], timeline["num_comments"], color=colors)
    plt.xticks(rotation=45)
    plt.title("Sentiment Timeline (Daily Comments & Emotional Tone)")
    plt.xlabel("Date")
    plt.ylabel("Number of Comments")
    plt.tight_layout()
    plt.savefig("output/sentiment_timeline.png")
    plt.close()


    # === PDF Creation ===
    class PDF(FPDF):
        def header(self):
            self.set_font("Arial", "B", 16)
            self.set_text_color(30, 30, 30)

        def chapter_title(self, title):
            self.ln(10)
            self.set_font("Arial", "B", 14)
            self.set_text_color(0, 0, 0)
            self.cell(0, 10, title, 0, 1)

        def chapter_body(self, body):
            self.set_font("Arial", "", 12)
            self.set_text_color(50, 50, 50)
            self.multi_cell(0, 10, body)
            self.ln()

        def add_image(self, image_path, w=180, h=100):
            self.image(image_path, x=15, y=self.get_y(), w=w, h=h)
            self.ln(h + 5)

    pdf = PDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 20)
    #pdf.cell(0, 10, "YouTube Comment Sentiment Analysis Report", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 14)
    pdf.multi_cell(0, 10, "This report provides an analysis of user engagement and emotional trends in YouTube comments.")


    pdf.chapter_title("1. Sentiment Distribution")
    pdf.chapter_body("The chart shows how user comments are spread across positive, neutral, and negative categories.")
    pdf.add_image("output/sentiment_distribution.png")


    pdf.chapter_title("2. Word Clouds by Sentiment")
    pdf.chapter_body("Each word cloud represents the most frequent words used in each sentiment category.")
    for label in sentiments:
        pdf.chapter_body(f"{label.capitalize()} Word Cloud:")
        pdf.add_image(f"output/wordcloud_{label}.png")


    pdf.chapter_title("3. Sentiment Timeline")
    pdf.chapter_body("This timeline shows how the sentiment of comments changes over time.")
    pdf.add_image("output/sentiment_timeline.png")



    pdf.chapter_title("4. Summary & Insights")
    summary = df["sentiment_label"].value_counts(normalize=True) * 100
    insight = (
        f"- Positive comments: {summary.get('positive', 0):.2f}%\n"
        f"- Neutral comments: {summary.get('neutral', 0):.2f}%\n"
        f"- Negative comments: {summary.get('negative', 0):.2f}%\n"
    )
    pdf.chapter_body(insight)

    pdf.output(output_path)
    print(f"✅ PDF report saved to {output_path}")
