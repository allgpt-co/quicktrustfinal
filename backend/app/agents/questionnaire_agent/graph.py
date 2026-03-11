"""Questionnaire auto-fill agent — orchestrates the pipeline."""
from langgraph.graph import StateGraph, END

from app.agents.questionnaire_agent.state import QuestionnaireAgentState
from app.agents.questionnaire_agent.nodes import (
    load_questionnaires,
    auto_fill_questionnaires,
    summarize_results,
)


def build_graph():
    """Build the LangGraph state graph for questionnaire auto-fill."""
    graph = StateGraph(QuestionnaireAgentState)

    graph.add_node("load_questionnaires", lambda state: state)
    graph.add_node("auto_fill_questionnaires", lambda state: state)
    graph.add_node("summarize_results", lambda state: state)

    graph.set_entry_point("load_questionnaires")
    graph.add_edge("load_questionnaires", "auto_fill_questionnaires")
    graph.add_edge("auto_fill_questionnaires", "summarize_results")
    graph.add_edge("summarize_results", END)

    return graph.compile()


async def run_questionnaire_agent(
    db,
    org_id: str,
    agent_run_id: str,
    questionnaire_id: str | None = None,
) -> dict:
    """
    Run the questionnaire auto-fill pipeline.
    If questionnaire_id is provided, processes only that questionnaire.
    Otherwise, processes all draft/in_progress questionnaires for the org.
    """
    state: QuestionnaireAgentState = {
        "org_id": org_id,
        "agent_run_id": agent_run_id,
        "questionnaire_id": questionnaire_id,
    }

    node_funcs = [
        ("load_questionnaires", load_questionnaires),
        ("auto_fill_questionnaires", auto_fill_questionnaires),
        ("summarize_results", summarize_results),
    ]

    for node_name, node_func in node_funcs:
        result = await node_func(state, db)
        if result:
            state.update(result)

        if state.get("error"):
            raise RuntimeError(state["error"])

    return {
        "total_filled": state.get("total_filled", 0),
        "total_questionnaires": state.get("total_questionnaires", 0),
        "results": state.get("results_by_questionnaire", []),
    }
