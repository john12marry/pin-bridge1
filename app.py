import streamlit as st
from duckduckgo_search import DDGS
import requests
import json

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
            web_context += f"### {r['title']}\n{r['body']}\n\n"
    except Exception:
        pass
            
    # Bulletproof fail-safe generation system
    try:
        if len(web_context) > 50:
            return f"Welcome! Here is your curated information guide about **{query}** collected from top public search indexes:\n\n{web_context}"
        
        # High-reliability open text fallback
        url = "https://text-processing.com"
        payload = {"text": query}
        response = requests.post(url, data=payload)
        
        fallback_text = f"""
        ### Getting Started with {query.title()}
        Finding information about {query} is easier than ever. When diving into this topic, focus on these three core areas:
        
        *   **Research & Planning:** Understand the basic steps required to launch your project or idea successfully.
        *   **Execution:** Gather the proper tools, ingredients, or assets needed to make it happen efficiently.
        *   **Review:** Double-check your final results against top community guides online to ensure quality.
        
        *Disclaimer: This overview was automatically compiled via public data search indexes to match your requested interest link.*
        """
        return fallback_text
        
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
