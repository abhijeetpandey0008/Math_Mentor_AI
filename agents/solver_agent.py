from utils.prompts import SOLVER_PROMPT
from utils.llm import generate_response
from rag.retriever import retrieve_docs


def solver_agent(state):

    # Problem extracted by parser
    problem = state["parsed_problem"]

    # Retrieve relevant knowledge from vector database
    docs = retrieve_docs(problem)

    # Combine retrieved docs into context
    context = "\n".join(docs)

    # Create prompt with context + problem
    prompt = SOLVER_PROMPT.format(
        context=context,
        problem=problem
    )

    # Generate solution using LLM
    solution = generate_response(prompt)

    # Store solution
    state["solution"] = solution

    # Store retrieved docs (for UI display)
    state["retrieved_docs"] = docs

    return state