import streamlit as st
from typing import Dict, Any
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from langsmith import traceable
from tavily import TavilyClient
import pandas as pd
import io
import os
import time

# ==========================================
# STREAMLIT UI
# ==========================================
st.set_page_config(page_title="AI Influencer Tracker", layout="wide")
st.title("🤖 AI Influencer Tracker (Ollama + Tavily + LangGraph + LangSmith)")

st.markdown("""
Use this tool to automatically discover and analyze top AI influencers across major platforms using your local Ollama model.
""")

# Input API keys
tavily_api = st.text_input("🔑 Enter your Tavily API Key:", type="password")
langsmith_api = st.text_input("🔑 Enter your LangSmith API Key (optional):", type="password")

if langsmith_api:
    os.environ["LANGSMITH_API_KEY"] = langsmith_api
if tavily_api:
    os.environ["TAVILY_API_KEY"] = tavily_api

# Platform selection
platforms = st.multiselect(
    "Select Platforms to Analyze:",
    ["LinkedIn", "X (Twitter)", "YouTube", "Instagram", "TikTok"],
    default=["LinkedIn", "X (Twitter)", "YouTube"]
)

# Model
MODEL_NAME = "gemma3:4b"
OUTPUT_CSV = "ai_influencer_tracker_2025.csv"

# ==========================================
# LANGGRAPH NODES
# ==========================================
class InfluencerState(Dict[str, Any]):
    platform: str
    search_results: str
    markdown_table: str

@traceable(name="Search Node")
def search_node(state: InfluencerState) -> InfluencerState:
    platform = state["platform"]
    st.write(f"🔍 Searching for **{platform} influencers**...")
    tavily = TavilyClient(api_key=tavily_api)
    query = f"Top AI influencers on {platform} in 2025 site:{platform.lower().split()[0]}.com"
    results = tavily.search(query, max_results=10)
    state["search_results"] = "\n\n".join([r["content"] for r in results["results"]])
    return state

@traceable(name="Summarizer Node")
def summarize_node(state: InfluencerState) -> InfluencerState:
    context = state["search_results"]
    platform = state["platform"]
    st.write(f"🧠 Summarizing influencers for {platform} using Gemma3:4...")

    model = ChatOllama(model=MODEL_NAME, temperature=0.3)
    prompt_template = PromptTemplate.from_template("""
You are an AI data researcher.
Using the text below, extract structured information about AI influencers active on {platform} in 2025.

Output a Markdown table with these columns:
| Name | Platform | Followers | Niche | Engagement | Content Type | Link | Source |

Context:
{context}
""")
    chain = prompt_template | model | StrOutputParser()
    state["markdown_table"] = chain.invoke({"platform": platform, "context": context})
    return state

@traceable(name="Writer Node")
def writer_node(state: InfluencerState) -> InfluencerState:
    markdown = state["markdown_table"]
    platform = state["platform"]

    lines = [line for line in markdown.splitlines() if "|" in line and "---" not in line]
    text = "\n".join(lines)
    try:
        df = pd.read_csv(io.StringIO(text), sep="|", skipinitialspace=True)
        df = df.dropna(how="all", axis=1).dropna(how="all", axis=0)
        df.columns = [c.strip() for c in df.columns]
        df["PlatformGroup"] = platform

        try:
            old_df = pd.read_csv(OUTPUT_CSV)
            df = pd.concat([old_df, df], ignore_index=True)
        except FileNotFoundError:
            pass

        df.to_csv(OUTPUT_CSV, index=False)
        st.success(f"✅ Saved {platform} influencers to {OUTPUT_CSV}")
    except Exception as e:
        st.error(f"⚠️ Failed to parse or write {platform} data: {e}")

    return state

# ==========================================
# BUILD LANGGRAPH
# ==========================================
graph = StateGraph(InfluencerState)
graph.add_node("search", search_node)
graph.add_node("summarize", summarize_node)
graph.add_node("writer", writer_node)

graph.add_edge("search", "summarize")
graph.add_edge("summarize", "writer")
graph.set_entry_point("search")
graph.set_finish_point("writer")

app = graph.compile()

# ==========================================
# RUN PIPELINE ON BUTTON CLICK
# ==========================================
if st.button("🚀 Run Influencer Tracker"):
    if not tavily_api:
        st.error("Please enter your Tavily API Key.")
    else:
        progress = st.progress(0)
        for i, platform in enumerate(platforms):
            state = {"platform": platform}
            app.invoke(state)
            time.sleep(3)
            progress.progress((i + 1) / len(platforms))
        st.success("🎉 All platform data collected successfully!")

        if os.path.exists(OUTPUT_CSV):
            df = pd.read_csv(OUTPUT_CSV)
            st.dataframe(df.head(20))
            st.download_button(
                "📥 Download CSV",
                data=open(OUTPUT_CSV, "rb"),
                file_name="ai_influencer_tracker_2025.csv",
                mime="text/csv"
            )
