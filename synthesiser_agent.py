try:
    from utils.llm_client import call_llm_large
except ImportError:
    # Fallback for older llm_client versions where call_llm_large may not exist
    from utils.llm_client import call_llm as call_llm_large

SYSTEM_PROMPT = """You are a world-class research analyst writing for MIT Technology Review.

Write a comprehensive, deeply analytical research report in Markdown.

REQUIRED STRUCTURE — include every section:

## Executive Summary
4-5 sentences. What is this topic, why does it matter right now, and what is the most important insight.

## Background & Context
2-3 paragraphs on origins, history, and why this topic exists. Include specific dates, events, and names.

## Key Findings
6-8 bullet points. Each bullet: **Bold label:** specific finding with concrete detail (2-3 sentences).

## Deep Analysis
4-5 paragraphs of original analysis. Each paragraph focuses on a distinct sub-theme.
Open each paragraph with a strong specific claim. Support with evidence. Minimum 100 words each.

## Challenges & Controversies
3-4 paragraphs on what does not work, genuine disagreements, limitations, and open questions.
Be intellectually honest — name specific barriers and unresolved problems.

## Real-World Applications
3-4 concrete examples with specific organisations, outcomes, and lessons learned.

## Future Outlook
3 specific predictions with reasoning. Bull case and bear case. What single development matters most.

## Conclusion
3 sentences: the single most important insight, and what a reader should do or think differently.

QUALITY RULES — mandatory:
- Every sentence must be specific to THIS topic. Never write something that applies to any topic.
- Include real names, organisations, dates, and numbers throughout.
- Minimum 1200 words total.
- Never use: "rapidly evolving", "it is worth noting", "in today's world", "various industries",
  "many experts", "several challenges", "significant implications", "needless to say"
- Write in active voice throughout."""


class SynthesiserAgent:

    def synthesise(self, topic: str, sources: list[dict]) -> str:

        sources_text = "\n\n".join([
            f"--- SOURCE [{i+1}] ---\n"
            f"Title: {s['title']}\n"
            f"Content: {s['snippet']}"
            for i, s in enumerate(sources)
        ])

        user_prompt = (
            f'Write a comprehensive research report about: "{topic}"\n\n'
            f'You have {len(sources)} sources below. Use them as grounding. '
            f'For any gaps in the sources, use your own expert knowledge about "{topic}" '
            f'to add specific facts, names, dates, and analysis.\n\n'
            f'SOURCES:\n{sources_text}\n\n'
            f'CRITICAL: Every paragraph must contain at least one specific fact that is '
            f'unique to "{topic}". Do not write generic filler. '
            f'Start directly with ## Executive Summary. No preamble.'
        )

        result = call_llm_large(
            SYSTEM_PROMPT,
            user_prompt,
            temperature=0.7,
            max_tokens=4096,
        )

        # Validate — if result is too short or looks like fallback, it means API call failed
        if (len(result.split()) < 100
                or "fallback" in result.lower()
                or "technical issues" in result.lower()):
            return self._emergency_synthesis(topic, sources)

        return result

    def _emergency_synthesis(self, topic: str, sources: list[dict]) -> str:
        """
        Direct call with minimal prompt — used when main call fails.
        Simpler prompt is less likely to hit token/timeout issues.
        """
        snippets = " ".join([s["snippet"][:300] for s in sources])
        prompt = (
            f"Write a detailed 1000-word research report about: {topic}\n\n"
            f"Reference material: {snippets}\n\n"
            f"Use markdown headers. Be specific and analytical. "
            f"Use your knowledge about {topic} to add depth beyond the reference material."
        )
        return call_llm_large(
            "You are an expert research analyst. Write detailed, specific reports.",
            prompt,
            temperature=0.7,
            max_tokens=3000,
        )