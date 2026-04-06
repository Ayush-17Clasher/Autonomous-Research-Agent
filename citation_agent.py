from utils.llm_client import call_llm
import re

SYSTEM_PROMPT = """You are a citation editor. You will receive a research report and a list of numbered sources.
Your job is to inject citation markers [1], [2], [3] etc. at appropriate points in the text 
where the source supports the claim being made.

Rules:
- Add citations INLINE after relevant sentences, like: "...emerging technology [1]." 
- Each source should be cited at least once if relevant
- Do NOT change the report's wording, structure, or content — ONLY add [n] markers
- Return the full report with citations added, nothing else"""


class CitationAgent:
    """
    Post-processes the synthesised report to inject inline citation
    markers [1], [2] etc. at semantically appropriate positions.
    """

    def cite(self, report: str, sources: list[dict]) -> str:
        if not sources:
            return report

        sources_list = "\n".join([
            f"[{i+1}] {s['title']} — {s['snippet'][:100]}"
            for i, s in enumerate(sources)
        ])

        user_prompt = f"""Add citation markers to this research report.

SOURCES:
{sources_list}

REPORT:
{report}

Return the full report with [n] citation markers added inline. Do not change any words."""

        try:
            cited = call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.1, max_tokens=2000)

            # Safety fallback: if LLM returns nothing useful, return original
            if len(cited.strip()) < len(report) * 0.5:
                return report

            return cited
        except Exception as e:
            # Fallback: return original report if citation fails
            return report
