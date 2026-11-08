from agents.research_agent import search_knowledge_base
from agents.analyst_agent import analyze_information


def test_research_finds_documents():
    results = search_knowledge_base("inteligencia artificial")

    assert len(results) > 0
    assert all("titulo" in item for item in results)


def test_research_returns_empty_for_unknown_topic():
    results = search_knowledge_base("xyzabc tema inexistente")

    assert results == []


def test_analyst_calculates_indicators():
    state = {
        "research_results": [
            {
                "titulo": "Beneficios de la automatización",
                "contenido": "Mejora la productividad."
            },
            {
                "titulo": "Riesgos de la inteligencia artificial",
                "contenido": "Puede generar sesgos."
            }
        ]
    }

    result = analyze_information(state)

    assert result["documents_analyzed"] == 2
    assert result["benefit_documents"] == 1
    assert result["risk_documents"] == 1
    assert result["coverage_percentage"] == 40.0
