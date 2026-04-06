from agents.query_planner import QueryPlannerAgent
from agents.search_agent import SearchAgent
from agents.synthesiser_agent import SynthesiserAgent
from agents.citation_agent import CitationAgent


class ResearchOrchestrator:
    """
    Orchestrates the full research pipeline:
    1. QueryPlannerAgent   → breaks topic into sub-queries
    2. SearchAgent         → fetches results for each sub-query
    3. SynthesiserAgent    → synthesises findings into a report
    4. CitationAgent       → injects numbered citations into report
    """

    def __init__(self, log_callback=None):
        self.log = log_callback or (lambda msg: None)
        self.query_planner = QueryPlannerAgent()
        self.search_agent = SearchAgent()
        self.synthesiser = SynthesiserAgent()
        self.citation_agent = CitationAgent()

    def run(self, topic: str, num_sources: int = 5) -> tuple[str, list[dict]]:
        self.log(f"Received topic: '{topic}'")

        # Step 1: Plan sub-queries
        self.log("QueryPlannerAgent → decomposing topic into sub-queries...")
        sub_queries = self.query_planner.plan(topic)
        self.log(f"Generated {len(sub_queries)} sub-queries: {', '.join(sub_queries[:3])}...")

        # Step 2: Search — fetch 2 results per query so we have enough
        # after deduplication to meet num_sources
        results_per_query = max(2, -(-num_sources // max(len(sub_queries), 1)) + 1)
        all_results = []

        for i, query in enumerate(sub_queries):
            self.log(f"SearchAgent → fetching results for query {i+1}: '{query}'")
            results = self.search_agent.search(query, max_results=results_per_query)
            all_results.extend(results)

        # Deduplicate by URL
        seen_urls = set()
        unique_results = []
        for r in all_results:
            if r["url"] not in seen_urls:
                seen_urls.add(r["url"])
                unique_results.append(r)

        # Take exactly num_sources (or all if fewer available)
        sources = unique_results[:num_sources]
        self.log(f"Collected {len(sources)} unique sources")

        # Step 3: Synthesise
        self.log("SynthesiserAgent → analysing and synthesising findings...")
        raw_report = self.synthesiser.synthesise(topic, sources)
        self.log("Synthesis complete")

        # Step 4: Add citations
        self.log("CitationAgent → injecting citations into report...")
        final_report = self.citation_agent.cite(raw_report, sources)
        self.log("Research pipeline complete ✓")

        return final_report, sources