from graph import app


def test_complete_multi_agent_workflow():
    initial_state = {
        "messages": [{"role": "user", "content": "Analizar inteligencia artificial"}],
        "user_query": "Analizar inteligencia artificial",
        "research_results": [],
        "analysis_results": {},
        "next_agent": "research",
        "iteration": 0,
        "max_iterations": 4,
        "validation": "",
        "final_answer": ""
    }

    result = app.invoke(initial_state)

    assert len(result["research_results"]) > 0
    assert result["analysis_results"]["documents_analyzed"] > 0
    assert result["next_agent"] == "finish"
    assert "INFORME FINAL" in result["final_answer"]
