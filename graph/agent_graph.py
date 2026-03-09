from langgraph.graph import StateGraph

from utils.schemas import GraphState

from agents.parser_agent import parser_agent
from agents.router_agent import router_agent
from agents.solver_agent import solver_agent
from agents.verifier_agent import verifier_agent
from agents.explainer_agent import explainer_agent


def build_graph():

    workflow = StateGraph(GraphState)

    workflow.add_node("parser", parser_agent)
    workflow.add_node("router", router_agent)
    workflow.add_node("solver", solver_agent)
    workflow.add_node("verifier", verifier_agent)
    workflow.add_node("explainer", explainer_agent)

    workflow.set_entry_point("parser")

    workflow.add_edge("parser", "router")
    workflow.add_edge("router", "solver")
    workflow.add_edge("solver", "verifier")
    workflow.add_edge("verifier", "explainer")

    return workflow.compile()