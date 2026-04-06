from utils.llm_client import call_llm
import json
import re

SYSTEM_PROMPT = """You are a research query planner. Given a research topic, generate focused sub-queries 
that together cover the topic comprehensively. Return ONLY a valid JSON array of strings — no explanation, 
no markdown, no preamble. Example: ["query one", "query two", "query three"]"""


class QueryPlannerAgent:
    """
    Breaks a broad research topic into 5 targeted sub-queries
    that will be searched independently for maximum coverage.
    """

    def plan(self, topic: str) -> list[str]:
        user_prompt = f"""Generate 5 focused search queries to research this topic comprehensively:

Topic: {topic}

Return ONLY a JSON array of 5 search query strings. No explanation."""

        try:
            response = call_llm(SYSTEM_PROMPT, user_prompt, temperature=0.3)

            try:
                # Extract JSON array from response
                match = re.search(r'\[.*?\]', response, re.DOTALL)
                if match:
                    queries = json.loads(match.group())
                    if isinstance(queries, list) and len(queries) > 0:
                        return [str(q) for q in queries]
            except (json.JSONDecodeError, ValueError):
                pass

            # Fallback: split on newlines if JSON parsing fails
            lines = [line.strip().strip('"').strip("'").strip('-').strip() 
                     for line in response.split('\n') if line.strip()]
            clean = [l for l in lines if len(l) > 10]
            return clean[:5] if clean else [topic]
        except Exception as e:
            # Fallback: return the original topic if LLM fails
            return [topic]
