from typing import TypedDict, List

class GraphState(TypedDict):

    question: str

    parsed_problem: str

    topic: str

    solution: str

    explanation: str

    confidence: float

    retrieved_docs: List[str]