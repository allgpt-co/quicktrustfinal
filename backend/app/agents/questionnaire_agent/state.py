from typing import TypedDict


class QuestionnaireAgentState(TypedDict, total=False):
    # Input
    org_id: str
    agent_run_id: str
    questionnaire_id: str | None

    # Intermediate
    questionnaires: list[dict]
    controls_context: str
    policies_context: str
    keyword_results: list[dict]
    llm_results: list[dict]

    # Output
    total_filled: int
    total_questionnaires: int
    results_by_questionnaire: list[dict]
    error: str | None
