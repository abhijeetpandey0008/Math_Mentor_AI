from utils.prompts import VERIFIER_PROMPT
from utils.llm import generate_response


def verifier_agent(state):

    solution = state["solution"]

    prompt = VERIFIER_PROMPT.format(solution=solution)

    response = generate_response(prompt)

    state["confidence"] = 0.9

    return state