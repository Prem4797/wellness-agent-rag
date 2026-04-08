from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Import the state we just created
from app.agents.state import AgentState

load_dotenv()

# Schema to force the LLM to output structured JSON
class IntakeOutput(BaseModel):
    is_specific: bool = Field(description="True if the user provided specific needs (e.g., a topic like burnout, or a language/price preference). False if vague.")
    topic: Optional[str] = Field(description="The core wellness topic or specialization requested (e.g., 'burnout', 'anxiety', 'career transition').")
    filters: Dict[str, Any] = Field(description="Extracted metadata filters. Keys can be 'price_range' (low/moderate/high), 'languages', 'location'. Empty dict if none mentioned.")
    follow_up_question: Optional[str] = Field(description="If is_specific is False, write a polite, empathetic follow-up question to clarify their needs.")

def intake_node(state: AgentState) -> dict:
    """Node 1: Analyzes intent and extracts metadata/topics with memory context."""
    print("--- NODE 1: INTAKE AGENT ---")
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    structured_llm = llm.with_structured_output(IntakeOutput)
    
    # We feed the previous state into the system prompt!
    system_msg = (
        "You are an expert Wellness Intake Coordinator. "
        "Your job is to extract search parameters from the user's LATEST message.\n\n"
        "CONTEXT FROM PREVIOUS MESSAGES:\n"
        "- Previous Topic: {prev_topic}\n"
        "- Previous Filters: {prev_filters}\n\n"
        "CRITICAL RULES:\n"
        "1. If the user is just updating a preference, combine old filters with the new ones.\n"
        "2. If the user asks for a new wellness issue, extract the new topic.\n"
        "3. OUT OF DOMAIN: If the user asks about coding, math, general trivia, or anything unrelated "
        "to wellness, mental health, or professional coaching, mark is_specific=False and politely "
        "explain that you are a Wellness AI and can only assist with finding professional support.\n"
        "4. If the wellness message is vague, mark is_specific=False and ask a follow-up."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", "{user_input}")
    ])
    
    chain = prompt | structured_llm
    
    # Pass the state variables into the prompt
    result: IntakeOutput = chain.invoke({
        "prev_topic": state.extracted_topic or "None",
        "prev_filters": state.extracted_filters or "None",
        "user_input": state.user_input
    })
    
    if result.is_specific:
        print(f"[Intake] Topic: {result.topic} | Filters: {result.filters}")
        return {
            "is_specific_enough": True,
            "extracted_topic": result.topic,
            "extracted_filters": result.filters,
            "final_response": ""
        }
    else:
        print(f"[Intake] Vague Need Detected. Asking follow-up.")
        return {
            "is_specific_enough": False,
            "final_response": result.follow_up_question
        }

# --- TEST BLOCK ---
if __name__ == "__main__":
    # Test 1: Vague Prompt
    print("\n--- TEST 1: Vague Input ---")
    vague_state = AgentState(user_input="I'm just really overwhelmed lately.")
    result_1 = intake_node(vague_state)
    print(f"Output Updates: {result_1}\n")

    # Test 2: Specific Prompt
    print("--- TEST 2: Specific Input ---")
    specific_state = AgentState(user_input="I am a software engineer facing burnout. I'd prefer someone who speaks Spanish and is moderately priced.")
    result_2 = intake_node(specific_state)
    print(f"Output Updates: {result_2}")