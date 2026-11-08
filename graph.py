from typing import Literal
from langgraph.graph import StateGraph, START, END
from state import AgentState
from agents.research_agent import research_agent
from agents.analyst_agent import analyst_agent


def supervisor(state: AgentState) -> dict:
    iteration = state.get("iteration", 0) + 1
    max_iterations = state.get("max_iterations", 4)

    print("\n[SUPERVISOR] Evaluando el estado del trabajo...")

    if iteration > max_iterations:
        return {
            "next_agent": "finish",
            "validation": "Se alcanzó el máximo de iteraciones.",
            "iteration": iteration
        }

    if not state.get("research_results"):
        next_agent = "research"
        validation = "Se necesita investigación."
    elif not state.get("analysis_results"):
        next_agent = "analyst"
        validation = "Investigación recibida. Se solicita análisis."
    else:
        next_agent = "finish"
        validation = "Los resultados de ambos especialistas fueron recibidos."

    print(f"[SUPERVISOR] Próximo paso: {next_agent}")

    return {
        "next_agent": next_agent,
        "validation": validation,
        "iteration": iteration
    }


def route_supervisor(
    state: AgentState
) -> Literal["research", "analyst", "finish"]:
    return state["next_agent"]


def finalizer(state: AgentState) -> dict:
    research = state.get("research_results", [])
    analysis = state.get("analysis_results", {})

    sources = "\n".join(
        f"- {doc['titulo']}: {doc['contenido']}"
        for doc in research
    )

    answer = f"""
INFORME FINAL DEL ORQUESTADOR

CONSULTA:
{state['user_query']}

INVESTIGACIÓN:
{sources if sources else 'No se encontraron documentos.'}

ANÁLISIS:
- Documentos analizados: {analysis.get('documents_analyzed', 0)}
- Documentos relacionados con beneficios: {analysis.get('benefit_documents', 0)}
- Documentos relacionados con riesgos: {analysis.get('risk_documents', 0)}
- Cobertura de la base: {analysis.get('coverage_percentage', 0)}%

VALIDACIÓN DEL SUPERVISOR:
{state.get('validation', '')}

CONCLUSIÓN:
El informe integra la información recuperada por Research Agent y los indicadores calculados por Analyst Agent.
Los resultados se limitan a la base de conocimiento local.
"""

    print("\n[SUPERVISOR] Informe final generado.")

    return {"final_answer": answer}


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("supervisor", supervisor)
    builder.add_node("research", research_agent)
    builder.add_node("analyst", analyst_agent)
    builder.add_node("finalizer", finalizer)

    builder.add_edge(START, "supervisor")

    builder.add_conditional_edges(
        "supervisor",
        route_supervisor,
        {
            "research": "research",
            "analyst": "analyst",
            "finish": "finalizer"
        }
    )

    builder.add_edge("research", "supervisor")
    builder.add_edge("analyst", "supervisor")
    builder.add_edge("finalizer", END)

    return builder.compile()


app = build_graph()
