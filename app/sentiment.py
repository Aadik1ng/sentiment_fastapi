# Content from D:\fastapi_sentiment_analysis\app\sentiment.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Directory where reports and charts will be saved
STATIC_DIR = "D:/fastapi_sentiment_analysis/static"

# Function to analyze sentiment using VADER
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)['compound']
    if sentiment_score >= 0.05:
        return 'Positive'
    elif sentiment_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Function to generate sentiment reports and save them to the static folder
def process_and_generate_report(file_contents: bytes):
    try:
        # Read the uploaded CSV file from bytes
        df = pd.read_csv(io.BytesIO(file_contents))

        # Ensure the 'text' column is present
        if 'text' not in df.columns:
            raise ValueError("CSV must contain a 'text' column.")
        
        # Apply sentiment analysis to each row
        df['sentiment'] = df['text'].apply(analyze_sentiment)

        # Generate Bar Chart
        sentiment_counts = df['sentiment'].value_counts()
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, palette='Set2', ax=ax)
        ax.set_title('Sentiment Distribution (Bar Chart)')
        ax.set_xlabel('Sentiment')
        ax.set_ylabel('Count')

        # Define file paths to save the chart
        bar_chart_filename = os.path.join(STATIC_DIR, "bar_chart.png")
        pie_chart_filename = os.path.join(STATIC_DIR, "pie_chart.png")

        # Save Bar Chart as PNG in the static folder
        fig.savefig(bar_chart_filename, format="png")
        plt.close(fig)

        # Generate Pie Chart
        fig, ax = plt.subplots(figsize=(8, 6))
        sentiment_counts.plot.pie(autopct='%1.1f%%', ax=ax, colors=['#FF9999', '#66B3FF', '#99FF99'])
        ax.set_title('Sentiment Distribution (Pie Chart)')
        ax.set_ylabel('')  # Remove ylabel for pie chart

        # Save Pie Chart as PNG in the static folder
        fig.savefig(pie_chart_filename, format="png")
        plt.close(fig)

        # Return the file paths for the saved charts
        return {
            "sentiment_counts": sentiment_counts.to_dict(),
            "positive_count": sentiment_counts.get('Positive', 0),
            "neutral_count": sentiment_counts.get('Neutral', 0),
            "negative_count": sentiment_counts.get('Negative', 0),
            "bar_chart_url": f"/static/bar_chart.png",  # Assuming the server serves static files from the static folder
            "pie_chart_url": f"/static/pie_chart.png"   # Same here for the pie chart
        }

    except Exception as e:
        raise ValueError(f"Error processing file: {str(e)}")
