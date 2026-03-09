from utils.prompts import ROUTER_PROMPT
from utils.llm import generate_response


def router_agent(state):

    problem = state["parsed_problem"]

    prompt = ROUTER_PROMPT.format(problem=problem)

    topic = generate_response(prompt)

    state["topic"] = topic

    return state