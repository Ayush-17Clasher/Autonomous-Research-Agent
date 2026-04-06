from unittest.mock import patch, MagicMock


# ── Query Planner ──────────────────────────────────────────
@patch("agents.query_planner.call_llm")
def test_query_planner_returns_list(mock_llm):
    mock_llm.return_value = '["query one", "query two", "query three"]'
    from agents.query_planner import QueryPlannerAgent
    agent = QueryPlannerAgent()
    result = agent.plan("quantum computing")
    assert isinstance(result, list)
    assert len(result) == 3


@patch("agents.query_planner.call_llm")
def test_query_planner_fallback(mock_llm):
    mock_llm.return_value = "invalid json response"
    from agents.query_planner import QueryPlannerAgent
    agent = QueryPlannerAgent()
    result = agent.plan("some topic")
    assert isinstance(result, list)
    assert len(result) >= 1


# ── Search Agent ───────────────────────────────────────────
def test_search_agent_mock_fallback():
    from agents.search_agent import SearchAgent
    agent = SearchAgent()
    results = agent._mock_results("test query", 3)
    assert len(results) == 3
    for r in results:
        assert "title" in r
        assert "url" in r
        assert "snippet" in r


# ── Synthesiser ────────────────────────────────────────────
@patch("agents.synthesiser_agent.call_llm")
def test_synthesiser_returns_string(mock_llm):
    mock_llm.return_value = "## Executive Summary\nTest report content."
    from agents.synthesiser_agent import SynthesiserAgent
    agent = SynthesiserAgent()
    sources = [{"title": "Test", "url": "http://test.com", "snippet": "Test snippet"}]
    result = agent.synthesise("test topic", sources)
    assert isinstance(result, str)
    assert len(result) > 0


# ── Citation Agent ─────────────────────────────────────────
@patch("agents.citation_agent.call_llm")
def test_citation_agent_adds_markers(mock_llm):
    mock_llm.return_value = "This is a cited report [1]. More content here [2]."
    from agents.citation_agent import CitationAgent
    agent = CitationAgent()
    sources = [
        {"title": "Source 1", "url": "http://s1.com", "snippet": "snippet 1"},
        {"title": "Source 2", "url": "http://s2.com", "snippet": "snippet 2"},
    ]
    result = agent.cite("Original report text.", sources)
    assert "[1]" in result or "[2]" in result


@patch("agents.citation_agent.call_llm")
def test_citation_agent_fallback(mock_llm):
    mock_llm.return_value = "x"  # too short — should fallback to original
    from agents.citation_agent import CitationAgent
    agent = CitationAgent()
    original = "This is a sufficiently long original report text that should be returned as fallback."
    sources = [{"title": "S", "url": "http://s.com", "snippet": "s"}]
    result = agent.cite(original, sources)
    assert result == original


# ── Formatter ──────────────────────────────────────────────
def test_formatter_converts_headers():
    from utils.formatter import format_report
    result = format_report("## Executive Summary\nSome text here.")
    assert "<h3" in result
    assert "Executive Summary" in result


def test_formatter_converts_citations():
    from utils.formatter import format_report
    result = format_report("Quantum computing is growing [1].")
    assert "<sup" in result
    assert "[1]" in result


def test_formatter_converts_bullets():
    from utils.formatter import format_report
    result = format_report("- First point\n- Second point")
    assert "<ul" in result
    assert "<li" in result
