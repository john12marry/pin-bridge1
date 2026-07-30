import streamlit as st
from duckduckgo_search import DDGS
import google.generativeai as genai

# Try to safely read your key from Streamlit Secrets vault
try:
    GEMINI_API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as vault_error:
    st.error(f"Vault Configuration Error: The server cannot find your key named 'GEMINI_KEY' inside the Streamlit Secrets vault. Details: {vault_error}")
    st.stop()

st.set_page_config(page_title="Instant Info Guide", layout="centered")

# Get the topic dynamically from the Pinterest URL parameter
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

# Fetch information with an automatic fallback mechanism
@st.cache_data(ttl=86400)
def generate_content(query):
    web_context = ""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        with DDGS(headers=headers) as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
        
        for r in results:
            web_context += f"Source: {r['title']}\nSnippet: {r['body']}\n\n"
    except Exception:
        pass
            
    # Try calling Gemini to write the text
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        You are an expert blogger. Write a short, highly engaging 250-word informational article about '{query}'.
        
        Optional real-time web facts to include if available:
        {web_context}
        
        Format the article beautifully with bold headings, short paragraphs, and clear bullet points.
        Add a small disclaimer at the bottom stating information was compiled from public data indexes.
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # Show the exact API failure reason right on screen
        return f"Gemini API Error: {str(e)}"

# Run the system and show the article
with st.spinner("Loading original insights..."):
    article_text = generate_content(search_query)
    st.markdown(article_text)

# PLACEHOLDER FOR YOUR FREE ADSENSE CODE (BOTTOM AD)
st.components.v1.html("""
    <div style="background-color: #f0f0f0; padding: 20px; text-align: center; border: 1px dashed #ccc; margin-top: 30px; font-family: sans-serif; font-size: 14px; color: #666;">
        [Sponsored Advertisement Slot]
    </div>
""", height=200)
