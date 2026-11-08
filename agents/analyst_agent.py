def analyze_information(state: dict) -> dict:
    documents = state.get("research_results", [])

    total = len(documents)
    risks = sum(
        1 for doc in documents
        if "riesgo" in (doc["titulo"] + doc["contenido"]).lower()
    )
    benefits = sum(
        1 for doc in documents
        if any(word in (doc["titulo"] + doc["contenido"]).lower()
               for word in ["beneficio", "productividad", "automatización"])
    )

    return {
        "documents_analyzed": total,
        "benefit_documents": benefits,
        "risk_documents": risks,
        "coverage_percentage": round((total / 5) * 100, 2)
    }


def analyst_agent(state: dict) -> dict:
    print("\n[ANALYST AGENT] Analizando resultados...")

    analysis = analyze_information(state)

    print("[ANALYST AGENT] Análisis completado.")

    return {
        "analysis_results": analysis,
        "messages": [{
            "role": "assistant",
            "content": f"Analyst Agent analizó {analysis['documents_analyzed']} documentos."
        }]
    }
