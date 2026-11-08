from typing import TypedDict, Literal
from langgraph.graph import MessagesState


class AgentState(MessagesState):
    user_query: str
    research_results: list
    analysis_results: dict
    next_agent: Literal["research", "analyst", "finish"]
    iteration: int
    max_iterations: int
    validation: str
    final_answer: str
