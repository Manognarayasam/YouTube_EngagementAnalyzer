# 📂 app.py

import streamlit as st
import os
import re
from scripts.fetch_comments import get_comments
from scripts.clean_comments import clean_text
import pandas as pd
from scripts.generate_report import generate_pdf_report

st.set_page_config(page_title="YouTube Sentiment Pipeline", layout="wide")
st.title("🔁 Full YouTube Comment Analysis Pipeline")
st.markdown("Enter a YouTube video ID or URL and run the full NLP pipeline.")

# === Extract Video ID from URL or input ===
def extract_video_id(link_or_id):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", link_or_id)
    return match.group(1) if match else link_or_id.strip().split('&')[0]

# === Input field ===
video_input = st.text_input("🎥 Enter YouTube Video ID or URL:")
video_id = extract_video_id(video_input)

if st.button("🚀 Run Full Pipeline"):
    if not video_id:
        st.error("❌ Please enter a YouTube Video ID.")
        st.stop()

    try:
        os.makedirs("data", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        with st.spinner("Step 1: Fetching comments..."):
            get_comments(video_id)
            st.success("✅ Comments fetched and saved to raw_comments.csv")

        with st.spinner("Step 2: Cleaning comments..."):
            df_raw = pd.read_csv("data/raw_comments.csv")
            df_raw["clean_text"] = df_raw["text"].apply(clean_text)
            df_raw.to_csv("data/cleaned_comments.csv", index=False)
            st.success("✅ Comments cleaned and saved to cleaned_comments.csv")

        with st.spinner("Step 3: Sentiment analysis..."):
            df = pd.read_csv("data/cleaned_comments.csv")
            df = df.dropna(subset=["clean_text"])
            df = df[df["clean_text"].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0)]

            from textblob import TextBlob
            df["sentiment_score"] = df["clean_text"].apply(lambda text: TextBlob(text).sentiment.polarity)

            def label_sentiment(score):
                if score > 0.1:
                    return "positive"
                elif score < -0.1:
                    return "negative"
                else:
                    return "neutral"

            df["sentiment_label"] = df["sentiment_score"].apply(label_sentiment)
            df.to_csv("data/sentiment_labeled_comments.csv", index=False)
            st.success("✅ Sentiment labeled and saved to sentiment_labeled_comments.csv")

        with st.spinner("Step 4: Generating report..."):
            generate_pdf_report(df)
            st.success("✅ Report generated and saved to output/sentiment_report.pdf")

    

        # === Download Report ===
        st.subheader("📄 Download Your Report")
        with open("output/sentiment_report.pdf", "rb") as f:
            st.download_button("📥 Download PDF", f, "sentiment_report.pdf")

    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
