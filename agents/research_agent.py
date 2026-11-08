import json
import re
from pathlib import Path


STOP_WORDS = {
    "para", "como", "sobre", "entre", "desde", "hasta",
    "este", "esta", "estos", "estas", "tema", "analizar",
    "analiza", "investiga", "informacion", "disponible",
    "una", "uno", "unos", "unas", "con", "por", "del",
    "las", "los", "que", "una", "empresa"
}


def tokenize(text: str) -> set:
    words = re.findall(r"[a-záéíóúñü]+", text.lower())

    return {
        word for word in words
        if len(word) > 3 and word not in STOP_WORDS
    }


def search_knowledge_base(query: str) -> list:
    path = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"

    with open(path, "r", encoding="utf-8-sig") as file:
        documents = json.load(file)

    query_terms = tokenize(query)

    if not query_terms:
        return []

    results = []

    for document in documents:
        text = (
            document["tema"] + " " +
            document["titulo"] + " " +
            document["contenido"]
        )

        document_terms = tokenize(text)
        matches = query_terms.intersection(document_terms)

        if matches:
            results.append({
                **document,
                "relevance": len(matches)
            })

    return sorted(
        results,
        key=lambda item: item["relevance"],
        reverse=True
    )[:5]


def research_agent(state: dict) -> dict:
    print("\n[RESEARCH AGENT] Buscando información...")

    results = search_knowledge_base(state["user_query"])

    print(f"[RESEARCH AGENT] Documentos encontrados: {len(results)}")

    return {
        "research_results": results,
        "messages": [{
            "role": "assistant",
            "content": f"Research Agent encontró {len(results)} documentos."
        }]
    }
