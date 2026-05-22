import streamlit as st
from langchain_config import get_summary

# Page settings
st.set_page_config(
    page_title="AI News Research Tool",
    page_icon="📰",
    layout="centered"
)

# Sidebar
st.sidebar.title("🧠 About")

st.sidebar.write("""
This AI-powered tool fetches latest news
and generates concise summaries using:

- Groq LLM
- NewsAPI
- Streamlit
""")

st.sidebar.info("Built by Tanya 🚀")

# Main title
st.title("📰 AI News Research Tool")

st.write("Get AI-powered summaries of latest news.")

# Category dropdown
category = st.selectbox(
    "📂 Select News Category",
    ["AI", "Technology", "Business", "Finance"]
)

# Input box
query = st.text_input(
    "🔍 Enter topic or company name",
    placeholder="Example: Tesla, Nvidia, OpenAI"
)

# Button
if st.button("🚀 Get News Summary"):

    if query:

        # Loading spinner
        with st.spinner("🤖 AI is researching latest news for you..."):

            final_query = f"{category} {query}"

            response, articles = get_summary(final_query)

        # Success message
        st.success("Summary generated successfully!")

        # Metrics row
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📰 Articles", len(articles))

        with col2:
            if "Positive" in response:
                st.metric("📈 Sentiment", "Positive")

            elif "Negative" in response:
                st.metric("📉 Sentiment", "Negative")

            else:
                st.metric("📊 Sentiment", "Neutral")

        with col3:
            st.metric("🔍 Topic", query.upper())

        # AI Summary
        st.subheader("🧠 AI Summary")

        # Sentiment badge
        if "Positive" in response:
            st.success("🟢 Positive Sentiment")

        elif "Negative" in response:
            st.error("🔴 Negative Sentiment")

        else:
            st.warning("🟡 Neutral Sentiment")

        st.info(response)

        # Articles section
        st.subheader("📰 Latest Articles")

        for article in articles:

            # Safe values
            title = article.get("title", "No Title")
            published = article.get("publishedAt", "N/A")
            source = article.get("source", {}).get("name", "Unknown")
            description = article.get("description", "No description available.")
            image = article.get("urlToImage")
            url = article.get("url", "#")

            # Styled article card
            st.html(f"""
            <div style="
                background-color:#1e1e1e;
                padding:20px;
                border-radius:15px;
                margin-bottom:25px;
            ">

                <h3 style="color:white;">
                    📰 {title}
                </h3>

                <p style="color:lightgray;">
                    📅 {published}
                </p>

                <p style="color:#bbbbbb;">
                    🏢 {source}
                </p>

                <p style="color:white;">
                    {description}
                </p>

                <a href="{url}" target="_blank"
                style="
                    color:#4da6ff;
                    text-decoration:none;
                    font-weight:bold;
                ">
                🔗 Read Full Article
                </a>

            </div>
            """)

            # Show image if available
            if image:
                st.image(image, use_container_width=True)

    else:
        st.warning("Please enter a topic.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Groq & NewsAPI")