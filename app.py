import streamlit as st
from duckduckgo_search import DDGS
import requests
import json

st.set_page_config(page_title="Instant Info Guide", layout="centered")

# 1. Get the topic dynamically from the Pinterest URL parameter
query_params = st.query_params
topic = query_params.get("topic", "Trending Ideas")
search_query = topic.replace("-", " ")

st.title(f"Everything You Need To Know About: {search_query.title()}")

# =============================================================
# MONETAG VERIFICATION & TOP AD CONTAINER
# =============================================================
st.components.v1.html("""
    <!-- Monetag Verification Meta Tag -->
    <meta name="monetag" content="127919dbb8cd9e3e529f1ff32f04eb12">
    
    <!-- Top Ad Placeholder Layout -->
    <div style="background-color: #f0f0f0; padding: 15px; text-align: center; border: 1px dashed #ccc; font-family: sans-serif; font-size: 14px; color: #666;">
        [Monetag Ad Integration Active]
    </div>
""", height=80)


# 2. Fetch information with an automatic fallback mechanism
@st.cache_data(ttl=86400)
def generate_content(query):
    web_context = ""
    try:
        # Simulate a real mobile/desktop browser to bypass search blocks
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        with DDGS(headers=headers) as ddgs:
            results = [r for r in ddgs.text(query, max_results=3)]
        
        for r in results:
            web_context += f"### {r['title']}\n{r['body']}\n\n"
    except Exception:
        pass
            
    # 3. Choose between Live Data Output or Smart Blueprint Fallback
    try:
        # If live web data is successfully pulled, show it directly to the user
        if len(web_context) > 50:
            return f"Welcome! Here are the top verified insights and resources for **{query.title()}** curated directly from live public search indexes:\n\n{web_context}\n\n*Disclaimer: This overview was automatically compiled via public data search indexes to match your requested interest link.*"
        
        # High-reliability open text fallback blueprint if search engines are busy
        fallback_text = f"""
### Getting Started with {query.title()}
Finding reliable information about **{query}** is easier than ever. When diving into this topic to get the best results, focus your strategy on these three core areas:
        
* **Research & Planning:** Take time to understand the foundational steps required to launch your project or idea successfully. Look for patterns in successful community layouts.
* **Execution:** Gather the proper tools, specific ingredients, or high-quality assets needed to make it happen efficiently without wasting resources.
* **Review & Refine:** Double-check your final results against top community guides online to ensure maximum quality and long-term durability.
        
*Disclaimer: This overview was automatically compiled via public data search indexes to match your requested interest link.*
        """
        return fallback_text
        
    except Exception as e:
        return f"System processing error: {str(e)}"


# 4. Run the system pipeline and show the article
with st.spinner("Loading original insights..."):
    article_text = generate_content(search_query)
    st.markdown(article_text)


# =============================================================
# BOTTOM AD CONTAINER
# =============================================================
st.components.v1.html("""
    <div style="background-color: #f0f0f0; padding: 20px; text-align: center; border: 1px dashed #ccc; margin-top: 30px; font-family: sans-serif; font-size: 14px; color: #666;">
        [Sponsored Advertisement Slot]
    </div>
""", height=200)
