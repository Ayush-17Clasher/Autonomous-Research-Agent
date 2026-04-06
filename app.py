import streamlit as st
import os

st.set_page_config(
    page_title="Autonomous Research Agent",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
.block-container { max-width: 960px; padding-top: 2rem; }
.source-card {
    background: #f8f9fa;
    border-left: 3px solid #4a90e2;
    padding: 0.6rem 1rem;
    margin: 0.4rem 0;
    border-radius: 0 6px 6px 0;
    font-size: 0.88rem;
}
.agent-step {
    background: #f0f4ff;
    border: 1px solid #dbe4ff;
    border-radius: 8px;
    padding: 0.5rem 0.9rem;
    margin: 0.3rem 0;
    font-size: 0.85rem;
    color: #3b5bdb;
}
.agent-error {
    background: #fff5f5;
    border: 1px solid #ffc9c9;
    border-radius: 8px;
    padding: 0.5rem 0.9rem;
    margin: 0.3rem 0;
    font-size: 0.85rem;
    color: #c92a2a;
}
.report-box {
    background: #ffffff;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 1.6rem 2rem;
    line-height: 1.85;
    font-size: 0.96rem;
}
.stat-pill {
    display: inline-block;
    background: #eef2ff;
    color: #3b5bdb;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.82rem;
    margin-right: 8px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

st.title("🔍 Autonomous Research Agent")
st.caption("Multi-agent pipeline · LLaMA 3 70B via Groq · Deep synthesis with citations")

# ── API Key check — show clear warning before user tries to run ──────────
def _load_env():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    k = k.strip(); v = v.strip().strip('"').strip("'")
                    if k and v and k not in os.environ:
                        os.environ[k] = v

_load_env()

if not os.environ.get("GROQ_API_KEY", "").strip():
    st.error(
        "**GROQ_API_KEY not found.**\n\n"
        "1. Get your free key at https://console.groq.com\n"
        "2. Open the `.env` file in your project folder\n"
        "3. Set it as: `GROQ_API_KEY=your_key_here`\n"
        "4. Save the file and **restart Streamlit** (`Ctrl+C` then `streamlit run app.py`)"
    )
    st.stop()

st.divider()

col1, col2 = st.columns([3, 1])
with col1:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Impact of World War 2 on global economics"
    )
with col2:
    depth = st.selectbox("Depth", ["Quick (3 sources)", "Standard (5 sources)", "Deep (8 sources)"])

depth_map = {"Quick (3 sources)": 3, "Standard (5 sources)": 5, "Deep (8 sources)": 8}
num_sources = depth_map[depth]

run = st.button("Research →", use_container_width=True, type="primary")

if run:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        st.divider()
        steps = []
        log_placeholder = st.empty()

        def log_step(msg, error=False):
            steps.append(("error" if error else "step", msg))
            html = ""
            for kind, text in steps:
                css = "agent-error" if kind == "error" else "agent-step"
                html += f'<div class="{css}">{"✗" if kind == "error" else "▸"} {text}</div>\n'
            log_placeholder.markdown(html, unsafe_allow_html=True)

        st.subheader("Agent activity")

        try:
            from agents.research_orchestrator import ResearchOrchestrator
            from utils.formatter import format_report

            with st.spinner("Running research pipeline — 30-60 seconds for deep analysis..."):
                orch = ResearchOrchestrator(log_callback=log_step)
                report, sources = orch.run(topic, num_sources=num_sources)

            word_count = len(report.split())
            section_count = report.count("## ")

            st.divider()
            st.markdown(
                f'<span class="stat-pill">📄 ~{word_count} words</span>'
                f'<span class="stat-pill">📑 {section_count} sections</span>'
                f'<span class="stat-pill">🔗 {len(sources)} sources</span>'
                f'<span class="stat-pill">🔎 {sources[0].get("source","?") if sources else "?"}</span>',
                unsafe_allow_html=True
            )

            st.subheader("Research report")
            st.markdown(
                f'<div class="report-box">{format_report(report)}</div>',
                unsafe_allow_html=True
            )

            st.divider()
            st.subheader(f"Sources ({len(sources)})")
            for i, src in enumerate(sources, 1):
                st.markdown(
                    f'<div class="source-card">'
                    f'<b>[{i}]</b> <a href="{src["url"]}" target="_blank">{src["title"][:80]}</a>'
                    f'<span style="color:#999;font-size:0.8rem;margin-left:8px">{src.get("source","?")}</span>'
                    f'<br><span style="color:#555">{src["snippet"][:160]}...</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            col_a, col_b = st.columns(2)
            with col_a:
                st.download_button(
                    "⬇ Download report (.md)",
                    data=report,
                    file_name=f"research_{topic[:40].replace(' ','_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
            with col_b:
                sources_txt = "\n".join([
                    f"[{i+1}] {s['title']}\n    {s['url']}\n" for i, s in enumerate(sources)
                ])
                st.download_button(
                    "⬇ Download sources (.txt)",
                    data=sources_txt,
                    file_name="sources.txt",
                    mime="text/plain",
                    use_container_width=True
                )

        except ValueError as e:
            st.error(f"Configuration error: {e}")
        except Exception as e:
            st.error(f"Pipeline error: {e}")
            st.info("Check that your GROQ_API_KEY is valid and you have internet access.")