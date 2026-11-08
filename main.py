import json
from datetime import datetime
from pathlib import Path
from graph import app


def main():
    print("=" * 60)
    print("ORQUESTADOR MULTI-AGENTE DE INVESTIGACIÓN Y ANÁLISIS")
    print("=" * 60)

    query = input("\nIngresá tu consulta: ").strip()

    if not query:
        print("La consulta no puede estar vacía.")
        return

    initial_state = {
        "messages": [{"role": "user", "content": query}],
        "user_query": query,
        "research_results": [],
        "analysis_results": {},
        "next_agent": "research",
        "iteration": 0,
        "max_iterations": 4,
        "validation": "",
        "final_answer": ""
    }

    print("\nIniciando orquestador...\n")

    trace = []
    final_answer = ""

    for event in app.stream(initial_state, stream_mode="updates"):
        for node, output in event.items():
            trace.append({
                "timestamp": datetime.now().isoformat(),
                "node": node,
                "output": output
            })

            if node == "finalizer":
                final_answer = output.get("final_answer", "")

    trace_data = {
        "query": query,
        "execution_date": datetime.now().isoformat(),
        "nodes_executed": [item["node"] for item in trace],
        "events": trace,
        "final_answer": final_answer
    }

    trace_path = Path("traces/execution_trace.json")
    trace_path.parent.mkdir(exist_ok=True)

    with open(trace_path, "w", encoding="utf-8") as file:
        json.dump(trace_data, file, ensure_ascii=False, indent=4, default=str)

    print("\n" + "=" * 60)
    print(final_answer or "No se generó un informe final.")
    print("=" * 60)

    print(f"\nTraza guardada en: {trace_path}")


if __name__ == "__main__":
    main()
