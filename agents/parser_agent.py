import json
from utils.prompts import PARSER_PROMPT
from utils.llm import generate_response


def parser_agent(state):

    question = state["question"]

    prompt = PARSER_PROMPT.format(question=question)

    response = generate_response(prompt)

    # Try parsing JSON response
    try:
        parsed = json.loads(response)
    except:
        parsed = {
            "problem_text": question,
            "topic_hint": None,
            "variables": [],
            "needs_clarification": False
        }

    state["parsed_problem"] = parsed["problem_text"]
    state["parser_output"] = parsed

    return state