import os
from dotenv import load_dotenv

# 1. Import the helper function from your vectorstore file!
from app.utils.vectorstore import get_vectorstore

# Import the state
from app.agents.state import AgentState

load_dotenv()

def retrieval_node(state: AgentState) -> dict:
    """Node 2: Executes the vector search based on extracted needs."""
    print("--- NODE 2: RETRIEVAL AGENT ---")
    
    # 2. Connect to ChromaDB using the Hugging Face model
    vectorstore = get_vectorstore()
    
    # Formulate the highly targeted Semantic Query
    filter_str = ", ".join([f"{k}: {v}" for k, v in state.extracted_filters.items()])
    search_query = f"Specialization: {state.extracted_topic}. Preferences: {filter_str}"
    
    print(f"[Retrieval] Searching Vector Store for: '{search_query}'")
    
    # Retrieve Top 3 Matches
    results = vectorstore.similarity_search(search_query, k=3)
    
    # Format the results to pass to the Synthesizer
    formatted_advisors = []
    for doc in results:
        formatted_advisors.append({
            "advisor_id": doc.metadata.get("advisor_id"),
            "profile_text": f"Bio: {doc.page_content} | Languages: {doc.metadata.get('languages', 'Not specified')} | Price: {doc.metadata.get('price_range', 'Not specified')}"
        })
        
    print(f"[Retrieval] Found {len(formatted_advisors)} matching advisors.")
    
    # Update the state with the retrieved list
    return {
        "retrieved_advisors": formatted_advisors
    }

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("\n--- TEST: Retrieval Node ---")
    
    test_state = AgentState(
        user_input="I am a software engineer facing burnout. I'd prefer someone who speaks Spanish and is moderately priced.",
        is_specific_enough=True,
        extracted_topic="burnout",
        extracted_filters={'languages': ['Spanish'], 'price_range': 'moderate'}
    )
    
    result = retrieval_node(test_state)
    
    print("\n--- Final Retrieved Profiles ---")
    for idx, adv in enumerate(result["retrieved_advisors"]):
        print(f"\nMatch {idx+1} (ID: {adv['advisor_id']}):")
        print(f"{adv['profile_text'][:200]}...")