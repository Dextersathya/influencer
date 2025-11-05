

---

# 🤖 AI Influencer Tracker

**(Ollama + Tavily + LangGraph + LangSmith + Streamlit)**

A powerful, AI-driven application that **automatically discovers, summarizes, and organizes top AI influencers** from major platforms like LinkedIn, X (Twitter), YouTube, Instagram, and TikTok — all powered by your **local Ollama model**.

Built using:
🧠 **Ollama** for local LLM reasoning
🔍 **Tavily API** for real-time web search
🧩 **LangGraph** for graph-based AI pipelines
📊 **Streamlit** for interactive dashboards
🧾 **LangSmith** for traceability and debugging

---

## 🚀 Key Features

✅ Fetch top AI influencers across multiple platforms
✅ Summarize and extract structured insights using local LLMs
✅ Automatically generate a clean, unified CSV report
✅ Modular LangGraph pipeline (Search → Summarize → Write)
✅ Streamlit dashboard for easy visualization & export

---

## 🧩 Architecture Overview

```
          ┌────────────────────────────────────┐
          │         Streamlit UI               │
          │ - User selects platforms           │
          │ - Displays results + download CSV  │
          └──────────────┬─────────────────────┘
                         │
         ┌───────────────┴────────────────────────┐
         │        LangGraph Workflow              │
         │   1️⃣ Search Node → Tavily API         │
         │   2️⃣ Summarizer Node → Ollama Model   │
         │   3️⃣ Writer Node → CSV Output         │
         └───────────────┬────────────────────────┘
                         │
             ┌───────────┴───────────┐
             │      Tavily API       │
             │   Web search results  │
             └───────────────────────┘
                         │
             ┌───────────┴───────────┐
             │       Ollama LLM      │
             │  (gemma3:4b or others)│
             └───────────────────────┘
```

---

## 🧰 Tech Stack

| Component              | Purpose                                            |
| ---------------------- | -------------------------------------------------- |
| **Streamlit**          | Interactive user interface                         |
| **LangGraph**          | Modular graph-based task flow                      |
| **LangSmith**          | Debugging and tracing LangChain calls              |
| **Tavily API**         | Fetches the latest influencer data from the web    |
| **Ollama (gemma3:4b)** | Generates structured summaries from search results |
| **Pandas**             | CSV parsing and analytics                          |

---

## 🛠️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Dextersathya/ai-influencer-tracker.git
cd ai-influencer-tracker
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
streamlit
tavily
pandas
langchain
langgraph
langsmith
langchain-ollama
```

---

## ⚙️ Setup

### 🔑 Required API Keys

You’ll need:

* **Tavily API Key:** [Get from Tavily](https://tavily.com)
* *(Optional)* **LangSmith API Key** for logging & tracing

You can set them directly in the Streamlit UI or export them as environment variables:

```bash
export TAVILY_API_KEY="your_tavily_api_key"
export LANGSMITH_API_KEY="your_langsmith_api_key"
```

---

## 🧠 Running the App

### 1️⃣ Start Ollama

Download Ollama and pull your model:

```bash
ollama pull gemma3:4b
ollama serve
```

### 2️⃣ Launch the Streamlit Dashboard

```bash
streamlit run app.py
```

or if your file is named differently:

```bash
streamlit run ai_influencer_tracker.py
```

### 3️⃣ Enter your API Keys and Select Platforms

In the Streamlit UI:

* Enter your Tavily API key
* (Optional) Enter your LangSmith key
* Choose platforms (LinkedIn, Twitter, YouTube, etc.)
* Click **🚀 Run Influencer Tracker**

---

## 📊 Output

Once complete, a file named:

```
ai_influencer_tracker_2025.csv
```

will be generated, containing influencer insights such as:

| Name        | Platform | Followers | Niche        | Engagement | Content Type    | Link   | Source |
| ----------- | -------- | --------- | ------------ | ---------- | --------------- | ------ | ------ |
| Andrew Ng   | LinkedIn | 2.3M      | AI Education | High       | Video, Post     | [link] | Tavily |
| Lex Fridman | YouTube  | 3.5M      | AI Podcast   | Very High  | Long-form Video | [link] | Tavily |

---

## 🧩 LangGraph Nodes

| Node             | Function  | Description                                        |
| ---------------- | --------- | -------------------------------------------------- |
| `search_node`    | Search    | Queries Tavily for AI influencers                  |
| `summarize_node` | Summarize | Uses Ollama (gemma3:4b) to extract influencer info |
| `writer_node`    | Write     | Saves structured data into CSV format              |

---

## ⚡ Example Output Log

```
🔍 Searching for LinkedIn influencers...
🧠 Summarizing influencers for LinkedIn using Gemma3:4...
✅ Saved LinkedIn influencers to ai_influencer_tracker_2025.csv
🔍 Searching for X (Twitter) influencers...
✅ Saved X (Twitter) influencers to ai_influencer_tracker_2025.csv
🎉 All platform data collected successfully!
```

---

## 🧩 Customization

You can modify the prompt template in the summarizer node:

```python
prompt_template = PromptTemplate.from_template("""
You are an AI data researcher.
Using the text below, extract structured information about AI influencers active on {platform} in 2025.

Output a Markdown table with these columns:
| Name | Platform | Followers | Niche | Engagement | Content Type | Link | Source |

Context:
{context}
""")
```

To:

* Add or remove columns
* Adjust tone or model temperature
* Switch to another Ollama model (e.g., `llama3`, `mistral`)

---

## 🧠 Future Enhancements

* 🧾 Multi-year trend tracking
* 📈 Sentiment & engagement scoring
* 🌍 Multi-language influencer discovery
* ☁️ Cloud deployment (Streamlit Cloud / Render / Railway)

---

## 👨‍💻 Author

**Dextersathya**
AI Engineer | Python Developer | Data Science Enthusiast
🔗 GitHub: [github.com/Dextersathya](https://github.com/Dextersathya)

---

## 🪪 License

This project is licensed under the **MIT License** — feel free to modify and build upon it.

---


