# Autonomous Research Agent — Complete Setup & Deployment Guide

---

## What this project does

You give it a research topic (e.g. "Impact of AI on healthcare in 2025").
It autonomously:
1. Breaks the topic into 5 focused sub-queries (QueryPlannerAgent)
2. Searches the web for each query (SearchAgent)
3. Synthesises all findings into a structured report (SynthesiserAgent)
4. Injects numbered citations into the report (CitationAgent)
5. Lets you download the report as Markdown

Stack: Python · LLaMA 3 via Groq · Streamlit · Docker · GitHub Actions CI

---

## Project structure

```
autonomous-research-agent/
├── app.py                          ← Streamlit UI
├── agents/
│   ├── research_orchestrator.py   ← Coordinates all agents
│   ├── query_planner.py           ← Breaks topic into sub-queries (LLM)
│   ├── search_agent.py            ← Fetches web results (DuckDuckGo)
│   ├── synthesiser_agent.py       ← Writes the report (LLM)
│   └── citation_agent.py          ← Adds inline citations (LLM)
├── utils/
│   ├── llm_client.py              ← Shared Groq/LLaMA 3 client
│   └── formatter.py               ← Markdown → HTML converter
├── tests/
│   └── test_agents.py             ← Unit tests (mocked LLM calls)
├── .github/workflows/ci.yml       ← GitHub Actions (test + docker build)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Step 1 — Get your free Groq API key

1. Go to https://console.groq.com
2. Sign up with your email (no credit card)
3. Click "Create API Key"
4. Copy the key — you'll use it in the next step

---

## Step 2 — Run locally (without Docker)

```bash
# Clone or unzip the project
cd autonomous-research-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Set your API key
cp .env.example .env
# Open .env and paste your GROQ_API_KEY

# Load env and run
export GROQ_API_KEY=your_key_here     # Mac/Linux
set GROQ_API_KEY=your_key_here        # Windows CMD

streamlit run app.py
```

App opens at http://localhost:8501

---

## Step 3 — Run with Docker

```bash
# Build the image
docker build -t autonomous-research-agent .

# Run the container
docker run -p 8501:8501 -e GROQ_API_KEY=your_key_here autonomous-research-agent
```

Or with docker-compose (easier):

```bash
# Set your key in .env file first, then:
docker-compose up --build
```

App runs at http://localhost:8501

---

## Step 4 — Run tests

```bash
# Tests use mocked LLM calls — no API key needed
pytest tests/ -v
```

All 9 tests should pass.

---

## Step 5 — Push to GitHub

```bash
# Initialise git
git init
git add .
git commit -m "feat: autonomous research agent with multi-agent pipeline"

# Create repo on github.com, then:
git remote add origin https://github.com/YOUR_USERNAME/autonomous-research-agent.git
git branch -M main
git push -u origin main
```

GitHub Actions will automatically run your tests on every push.

---

## Step 6 — Deploy free on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click "New app"
3. Select your GitHub repo → branch: main → file: app.py
4. Click "Advanced settings" → Secrets → add:
   ```
   GROQ_API_KEY = "your_key_here"
   ```
5. Click Deploy

Your app gets a public URL like:
`https://your-username-autonomous-research-agent.streamlit.app`

**Add this URL to your resume and GitHub README.**

---

## Step 7 — Update your resume

Add this under Projects:

> **Autonomous Web Research Agent** · github.com/YOUR_USERNAME/autonomous-research-agent
> Built a production multi-agent AI system using LangGraph-style orchestration, LLaMA 3 (Groq),
> and DuckDuckGo search to autonomously research any topic and generate cited reports.
> Stack: Python, Groq API, Streamlit, Docker, GitHub Actions CI. Deployed on Streamlit Cloud.

---

## How the agent pipeline works (for interviews)

```
User enters topic
        ↓
QueryPlannerAgent  →  LLaMA 3 breaks topic into 5 sub-queries
        ↓
SearchAgent (×5)   →  DuckDuckGo fetches real web results per query
        ↓
SynthesiserAgent   →  LLaMA 3 synthesises all snippets into structured report
        ↓
CitationAgent      →  LLaMA 3 injects [1][2][3] citation markers inline
        ↓
Streamlit UI       →  Displays report + sources + download buttons
```

Each agent has one job. They don't know about each other.
The Orchestrator is the only one that knows the full pipeline.
This is the single responsibility principle applied to AI agents.

---

## Environment variables reference

| Variable      | Required | Description                        |
|---------------|----------|------------------------------------|
| GROQ_API_KEY  | Yes      | Free key from console.groq.com     |

---

## Extending the project (ideas for interview discussions)

- Add Redis caching so repeated queries don't re-fetch
- Add a FactCheckerAgent that cross-references claims
- Replace DuckDuckGo with SerpAPI for richer results
- Add ChromaDB to store past research sessions
- Add streaming so the report appears word by word
- Add a PDF export using reportlab or weasyprint
- Add LangSmith for agent trace observability
