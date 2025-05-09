## YouTube Sentiment Analyzer Dashboard

This project is a full-stack **NLP pipeline** built with **Streamlit** that analyzes public YouTube comments from any video, performs **sentiment classification**, and presents results in an interactive dashboard.

###  Features

- Enter any YouTube video ID or URL to fetch recent comments
- Clean and normalize comment text
- Perform sentiment analysis using **TextBlob**
- Visualize results with:
    - Sentiment distribution chart
    - Word clouds by sentiment
    - Summary statistics

---

###  How It Works

### 1. Run Pipeline

From the sidebar:

- Enter a YouTube video ID or full URL
- Click **Run Full Pipeline** to:
    - Fetch up to 500 comments
    - Clean and tokenize them
    - Score sentiment polarity
    - Categorize into positive, neutral, or negative
    - Save results to `data/` directory

### 2. View Dashboard

Navigate to the **Dashboard** tab to see:

- A bar chart showing sentiment split
- Word clouds for each sentiment category
- Textual summary of proportions

---

### File Structure

```
📂 scripts/
├── fetch_comments.py        # Fetches YouTube comments using API
├── clean_comments.py        # Contains clean_text() function
├── sentiment_analysis.py    # (Optional) legacy logic
├── generate_report.py       # (Not used in current UI)can use It IF you want to generate reports
📂 data/
├── raw_comments.csv
├── cleaned_comments.csv
├── sentiment_labeled_comments.csv
📂 output/
applicatio.py                       # Streamlit UI
app.py                              #pdf version application
requirements.txt
README.md

```

---

### Setup Instructions

1. **Install dependencies**
    
    ```bash
    pip install -r requirements.txt
    
    ```
    
2. **Set your YouTube API key**
Create a `.env` file with:
    
    ```
    YOUTUBE_API_KEY=your_api_key_here
    
    ```
    
3. **Run the app**
    
    ```bash
    streamlit run app.py
    
    ```
    

---

### Notes

- Only public videos with comments enabled are supported
- Up to 500 top-level comments will be fetched
