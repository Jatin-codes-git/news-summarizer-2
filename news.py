import streamlit as st
from newspaper import Article
from textblob import TextBlob
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer


# Function to extract article text
def get_article_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        return f"Error fetching article: {e}"


# Function to summarize text
def summarize_text(text):
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, 5)
        summary = " ".join(str(sentence) for sentence in summary_sentences)
        return summary
    except Exception as e:
        return f"Error summarizing article: {e}"


# Function to analyze sentiment
def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            return "😊 Positive"
        elif polarity < 0:
            return "😞 Negative"
        else:
            return "😐 Neutral"
    except Exception as e:
        return f"Error analyzing sentiment: {e}"


# Streamlit UI
st.markdown("<h1 style='text-align: center; color: #1E88E5;'>📰 News Summarizer & Sentiment Analyzer 💡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Enter a news article URL to get its <span style='color: #43A047;'>summary</span> and <span style='color: #FB8C00;'>sentiment</span> analysis:</p>", unsafe_allow_html=True)

url = st.text_input("🔗 Enter the URL of the news article:")

if st.button("🚀 Summarize and Analyze"):
    if url:
        with st.spinner("⏳ Processing..."):
            article_text = get_article_text(url)
            if "Error" in article_text:
                st.error("❌ " + article_text)
            else:
                st.markdown("<h3 style='color: #3949AB;'>📝 Original Article:</h3>", unsafe_allow_html=True)
                st.write(article_text)

                summary = summarize_text(article_text)
                if "Error" in summary:
                    st.error("❌ " + summary)
                else:
                    st.markdown("<h3 style='color: #00897B;'>📌 Summary:</h3>", unsafe_allow_html=True)
                    st.write(summary)

                    sentiment = analyze_sentiment(summary)
                    st.markdown("<h3 style='color: #F4511E;'>🎭 Sentiment of the Summary:</h3>", unsafe_allow_html=True)
                    st.write(sentiment)
    else:
        st.warning("⚠️ Please enter a valid URL.")
