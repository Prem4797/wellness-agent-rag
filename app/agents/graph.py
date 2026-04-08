from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

# Import our State
from app.agents.state import AgentState

# Import our individual Node functions
from app.agents.intake_agent import intake_node
from app.agents.retrieval_agent import retrieval_node
from app.agents.synthesizer_agent import synthesizer_node

load_dotenv()

def route_after_intake(state: AgentState) -> str:
    """
    Conditional router that decides what to do after the Intake Agent.
    """
    if state.is_specific_enough:
        print("--> [Router] Intent is specific. Routing to Retrieval Agent.")
        return "retrieval"
    else:
        print("--> [Router] Intent is vague. Routing to END to ask follow-up.")
        return "end"

def get_compiled_graph():
    """Builds and compiles the LangGraph workflow with Memory."""
    
    # 1. Initialize the StateGraph with our Pydantic schema
    workflow = StateGraph(AgentState)

    # 2. Add our nodes (the agents)
    workflow.add_node("intake", intake_node)
    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("synthesizer", synthesizer_node)

    # 3. Define the Flow (Edges)
    # Everything starts at the intake agent
    workflow.set_entry_point("intake")

    # The Intake agent decides if we search or ask a follow-up
    workflow.add_conditional_edges(
        "intake",
        route_after_intake,
        {
            "retrieval": "retrieval", # If router returns "retrieval", go to retrieval node
            "end": END                # If router returns "end", stop the graph
        }
    )

    # After retrieval, we MUST synthesize the response
    workflow.add_edge("retrieval", "synthesizer")
    
    # After synthesis, the workflow is complete
    workflow.add_edge("synthesizer", END)

    # INITIALIZE MEMORY
    memory = MemorySaver()
    
    # 4. Compile the graph
    app = workflow.compile(checkpointer=memory)
    
    return app

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("\n================ COMPILING AGENT GRAPH ================\n")
    agent_app = get_compiled_graph()
    
    # --- ADD THIS LINE TO SEE THE MERMAID GRAPH ---
    print(agent_app.get_graph().draw_mermaid())
    print("\n=======================================================\n")
    
    # TEST 1: The Vague User
    print("\n--- SIMULATION 1: VAGUE INPUT ---")
    state_1 = AgentState(user_input="I just feel really lost and need someone to talk to.")
    # Run the graph
    result_1 = agent_app.invoke(state_1)
    print("\n[FINAL SYSTEM OUTPUT]:")
    print(result_1["final_response"])
    
    print("\n" + "="*50 + "\n")

    # TEST 2: The Specific User
    print("\n--- SIMULATION 2: SPECIFIC INPUT ---")
    state_2 = AgentState(user_input="I'm dealing with severe project deadline anxiety. I need someone cheap who speaks English.")
    # Run the graph
    result_2 = agent_app.invoke(state_2)
    print("\n[FINAL SYSTEM OUTPUT]:")
    print(result_2["final_response"])