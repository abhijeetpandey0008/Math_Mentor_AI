from utils.prompts import EXPLAINER_PROMPT
from utils.llm import generate_response


def explainer_agent(state):

    solution = state["solution"]

    prompt = EXPLAINER_PROMPT.format(solution=solution)

    explanation = generate_response(prompt)

    state["explanation"] = explanation

    return state