import streamlit as st
import os
import re
from scripts.fetch_comments import get_comments
from scripts.clean_comments import clean_text
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(page_title="YouTube Sentiment Pipeline", layout="wide")

# === Page Navigation ===
page = st.sidebar.selectbox(" Select Page", ["Run Pipeline", " Dashboard"])

# === Extract Video ID ===
def extract_video_id(link_or_id):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", link_or_id)
    return match.group(1) if match else link_or_id.strip().split('&')[0]

# === Dashboard Display Function ===
def show_dashboard():
    st.title("Sentiment Analysis Dashboard")
    try:
        df = pd.read_csv("data/sentiment_labeled_comments.csv")

        # === Distribution ===
        st.subheader("Sentiment Distribution")
        fig1, ax1 = plt.subplots()
        sns.countplot(data=df, x="sentiment_label", order=["positive", "neutral", "negative"], ax=ax1)
        st.pyplot(fig1)

        # === Word Clouds ===
        st.subheader("Word Clouds by Sentiment")
        for label in ["positive", "neutral", "negative"]:
            texts = df[df["sentiment_label"] == label]["clean_text"].dropna()
            texts = texts[texts.str.strip().astype(bool)]
            if len(texts) > 0:
                wc = WordCloud(width=800, height=400, background_color="white").generate(" ".join(texts))
                st.markdown(f"**{label.capitalize()} Comments**")
                st.image(wc.to_array(), use_column_width=True)
            else:
                st.warning(f" No valid {label} comments to display.")

        # === Summary Stats ===
        st.subheader(" Summary")
        summary = df["sentiment_label"].value_counts(normalize=True) * 100
        for label in ["positive", "neutral", "negative"]:
            st.markdown(f"**{label.capitalize()}**: {summary.get(label, 0):.2f}%")

    except FileNotFoundError:
        st.warning("No sentiment_labeled_comments.csv file found. Please run the pipeline first.")

if page == "Run Pipeline":
    st.title("Full YouTube Comment Analysis Pipeline")
    st.markdown("Enter a YouTube video ID or URL and run the full NLP pipeline.")

    video_input = st.text_input("🎥 Enter YouTube Video ID or URL:")
    video_id = extract_video_id(video_input)

    if st.button("Run Full Pipeline"):
        if not video_id:
            st.error(" Please enter a YouTube Video ID.")
            st.stop()

        try:
            os.makedirs("data", exist_ok=True)
            os.makedirs("output", exist_ok=True)

            with st.spinner("Step 1: Fetching comments..."):
                get_comments(video_id)
                st.success("Comments fetched and saved to raw_comments.csv")

            with st.spinner("Step 2: Cleaning comments..."):
                df_raw = pd.read_csv("data/raw_comments.csv")
                df_raw["clean_text"] = df_raw["text"].apply(clean_text)
                df_raw.to_csv("data/cleaned_comments.csv", index=False)
                st.success("Comments cleaned and saved to cleaned_comments.csv")

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
                st.success("Sentiment labeled and saved to sentiment_labeled_comments.csv")

        except Exception as e:
            st.error(f" Unexpected error: {e}")

elif page == " Dashboard":
    show_dashboard()