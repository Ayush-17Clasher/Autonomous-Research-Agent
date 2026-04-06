# 🔍 Autonomous Web Research Agent

An AI-powered multi-agent system that autonomously researches any topic — breaking it into sub-queries, searching the web, synthesising findings, and generating a fully cited research report.

![CI](https://github.com/YOUR_USERNAME/autonomous-research-agent/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11-blue)
![LLM](https://img.shields.io/badge/LLM-LLaMA%203%20via%20Groq-orange)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

**[Live Demo →](https://your-app.streamlit.app)**

---

## How it works

```
Topic input
    ↓
QueryPlannerAgent   →  LLaMA 3 decomposes topic into 5 targeted sub-queries
    ↓
SearchAgent (×N)    →  DuckDuckGo fetches real web results per query
    ↓
SynthesiserAgent    →  LLaMA 3 synthesises findings into structured Markdown report
    ↓
CitationAgent       →  LLaMA 3 injects inline [1][2][3] citation markers
    ↓
Streamlit UI        →  Renders report + sources + download buttons
```

Each agent has a single responsibility. The `ResearchOrchestrator` coordinates the pipeline without any agent knowing about the others.

## Tech stack

| Layer | Technology |
|-------|-----------|
| LLM | LLaMA 3 8B via Groq API (free) |
| Agent orchestration | Custom multi-agent pipeline |
| Web search | DuckDuckGo Instant Answer API (free, no key) |
| Frontend | Streamlit |
| Containerisation | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Testing | Pytest with mocked LLM calls |
| Hosting | Streamlit Cloud (free) |

## Quick start

```bash
git clone https://github.com/YOUR_USERNAME/autonomous-research-agent.git
cd autonomous-research-agent

pip install -r requirements.txt

export GROQ_API_KEY=your_free_key_from_console.groq.com

streamlit run app.py
```

## Run with Docker

```bash
docker build -t autonomous-research-agent .
docker run -p 8501:8501 -e GROQ_API_KEY=your_key autonomous-research-agent
```

## Run tests

```bash
pytest tests/ -v
```

## Project structure

```
├── app.py                         # Streamlit UI
├── agents/
│   ├── research_orchestrator.py  # Pipeline coordinator
│   ├── query_planner.py          # Topic → sub-queries (LLM)
│   ├── search_agent.py           # Web search (DuckDuckGo)
│   ├── synthesiser_agent.py      # Findings → report (LLM)
│   └── citation_agent.py         # Inline citation injection (LLM)
├── utils/
│   ├── llm_client.py             # Shared Groq client
│   └── formatter.py              # Markdown → HTML
├── tests/test_agents.py          # Unit tests
├── .github/workflows/ci.yml      # CI pipeline
├── Dockerfile
└── docker-compose.yml
```

---

Built by [Ayush Tripathi](https://linkedin.com/in/ayush-tripathi-16699b197)
