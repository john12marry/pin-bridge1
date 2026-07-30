import streamlit as st
from duckduckgo_search import DDGS
import requests

# 1. Load and automatically repair your API Key configuration
try:
    raw_key = st.secrets["GEMINI_KEY"]
    # If the key is missing the required Google prefix, fix it automatically
    if not raw_key.startswith("AIzaSy"):
        GEMINI_API_KEY = f"AIzaSy{raw_key}"
    else:
        GEMINI_API_KEY = raw_key
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
            
    # Completely separated URL structure to stop connection pool errors
    try:
        url = "https://googleapis.com"
        
        prompt = f"You are an expert blogger. Write a short, highly engaging 250-word informational article about '{query}'. Use these facts if helpful:\n{web_context}\nFormat beautifully with bold headings, short paragraphs, and bullet points. Add a small disclaimer at the bottom stating information was compiled from public data indexes."
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": GEMINI_API_KEY
        }
        
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        
        if "error" in res_data:
            return f"Google Server Message: {res_data['error']['message']}"
            
        return res_data["candidates"][0]["content"]["parts"][0]["text"]
        
    except Exception as e:
        return f"System processing error: {str(e)}"

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
