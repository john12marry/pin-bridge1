import import streamlit as st
from duckduckgo_search import DDGS
import google.generativeai as genai

# 1. Securely load your free Gemini API Key from Streamlit Secrets
GEMINI_API_KEY = st.secrets["GEMINI_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="Instant Info Guide", layout="centered")

# 2. Get the topic dynamically from the Pinterest URL parameter
query_params = st.query_params
topic = query_params.get("topic", "Trending Ideas")
search_query = topic.replace("-", " ")

st.title(f"Everything You Need To Know About: {search_query.title()}")

# PLACEHOLDER FOR YOUR FREE ADSENSE CODE (TOP AD)
st.components.v1.html("""
    <div style="background-color: #f0f0f0; padding: 15px; text-align: center; border: 1px dashed #ccc; font-family: sans-serif; font-size: 14px; color: #666;">
        [Sponsored Advertisement Slot]
    </div>
""", height=80)

# 3. Fetch information for FREE using DuckDuckGo Search
@st.cache_data(ttl=86400)
def generate_content(query):
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
        
        web_context = ""
        for r in results:
            web_context += f"Source: {r['title']}\nSnippet: {r['body']}\n\n"
            
        # 4. Use Gemini Flash (Free Tier) to rewrite the data into a blog post
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        You are an expert blogger. Write a short, highly engaging 250-word informational article about '{query}'.
        Use the following real-time web facts to ensure accurate details:
        {web_context}
        
        Format the article with bold headings, short paragraphs, and bullet points so it looks highly professional.
        Add a small disclaimer at the bottom stating information was summarized from public search indexes.
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return "Loading content... Please refresh in a moment."

# Run the functions and display the freshly generated text
with st.spinner("Loading original insights..."):
    article_text = generate_content(search_query)
    st.markdown(article_text)

# PLACEHOLDER FOR YOUR FREE ADSENSE CODE (BOTTOM AD)
st.components.v1.html("""
    <div style="background-color: #f0f0f0; padding: 20px; text-align: center; border: 1px dashed #ccc; margin-top: 30px; font-family: sans-serif; font-size: 14px; color: #666;">
        [Sponsored Advertisement Slot]
    </div>
""", height=200)
