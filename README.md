

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

