from dotenv import load_dotenv
import os

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from newsapi import NewsApiClient

# Load environment variables
load_dotenv()

# API Keys
groq_api_key = os.getenv("GROQ_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

# Initialize NewsAPI
newsapi = NewsApiClient(api_key=news_api_key)

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model_name="llama-3.1-8b-instant"
)

# Fetch news articles
def get_news_articles(query):

    articles = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="relevancy",
        page_size=5
    )

    return articles["articles"]

# Combine summaries
def summarize_articles(articles):

    summaries = []

    for article in articles:

        if article["description"]:

            summaries.append(article["description"])

    return " ".join(summaries)

# Main function
def get_summary(query):

    articles = get_news_articles(query)

    summaries = summarize_articles(articles)

    # Prompt template
    template = """
You are an AI financial news analyst.

Analyze the following news summaries.

Query: {query}

News summaries:
{summaries}

Tasks:
1. Provide a concise overall summary.
2. Determine the overall sentiment:
   - Positive
   - Negative
   - Neutral

Format your response exactly like this:

Sentiment: <sentiment>

Summary:
<summary>
"""

    prompt = PromptTemplate.from_template(template)

    final_prompt = prompt.format(
        query=query,
        summaries=summaries
    )

    response = llm.invoke(final_prompt)

    return response.content, articles
