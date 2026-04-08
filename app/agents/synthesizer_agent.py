from pydantic import BaseModel, Field
from typing import List
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from app.agents.state import AgentState

load_dotenv()

# --- 1. Define the Structured JSON Schema ---
class AdvisorRecommendation(BaseModel):
    name: str = Field(description="The name of the advisor, including their ID if available (e.g., 'Dr. Smith (ID: 123)').")
    description: str = Field(description="A brief, empathetic explanation of why this advisor is a good match for the user.")

class SynthesizerOutput(BaseModel):
    intro: str = Field(description="The warm, empathetic introduction, including the disclaimer that you are an AI and not a medical professional.")
    advisors: List[AdvisorRecommendation] = Field(description="The list of recommended advisors.")
    outro: str = Field(description="The supportive closing message.")

def synthesizer_node(state: AgentState) -> dict:
    """Node 3: Drafts the final empathetic response in strict JSON format."""
    print("--- NODE 3: SYNTHESIZER AGENT ---")
    
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.4)
    # Force the LLM to output the Pydantic schema
    structured_llm = llm.with_structured_output(SynthesizerOutput)
    
    # Format the retrieved advisors into a readable string for the LLM to process
    formatted_profiles = ""
    for idx, adv in enumerate(state.retrieved_advisors):
        formatted_profiles += f"\nOption {idx+1}:\nID: {adv.get('advisor_id')}\nDetails: {adv.get('profile_text')}\n"
        
    system_msg = (
        "You are an empathetic and professional Wellness Matchmaker AI. "
        "Your goal is to present the retrieved advisor profiles to the user in a warm, encouraging manner. "
        "\n\nCRITICAL GUARDRAILS:"
        "\n1. You MUST include a brief disclaimer in the intro that you are an AI assistant, not a medical professional."
        "\n2. Do NOT diagnose the user."
        "\n3. Present the advisors clearly, highlighting WHY they are a good match based on the user's prompt."
        "\n4. Keep the tone supportive but concise."
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_msg),
        ("human", "Overall Topic Searched: {topic}\nUser's Latest Request: {user_input}\n\nRetrieved Advisors to Recommend: {advisors}")
    ])
    
    chain = prompt | structured_llm
    
    # Generate the structured response
    result: SynthesizerOutput = chain.invoke({
        "topic": state.extracted_topic,
        "user_input": state.user_input,
        "advisors": formatted_profiles
    })
    
    print("[Synthesizer] Final structured JSON response drafted successfully.")
    
    # Update the state with the dictionary output (model_dump converts Pydantic to a standard Python dict)
    return {
        "final_response": result.model_dump()
    }

# --- TEST BLOCK ---
if __name__ == "__main__":
    print("\n--- TEST: Synthesizer Node ---")
    
    test_state = AgentState(
        user_input="I am a software engineer facing burnout. I'd prefer someone who speaks Spanish and is moderately priced.",
        retrieved_advisors=[
            {
                "advisor_id": "48",
                "profile_text": "Advisor Name: Sasha Petrov. Specializes in open source maintainer burnout, developer community stress. Bio: Sasha supports open-source maintainers who deal with the emotional labor of tech. Languages: Spanish, English. Price: moderate."
            },
            {
                "advisor_id": "59",
                "profile_text": "Advisor Name: Lucia Mendez. Specializes in HR director burnout, workplace culture fatigue. Bio: Lucia supports professionals navigating company-wide restructures. Languages: Spanish. Price: moderate."
            }
        ]
    )
    
    result = synthesizer_node(test_state)
    import json
    print("\n================ FINAL AI JSON RESPONSE ================\n")
    print(json.dumps(result["final_response"], indent=2))
    print("\n========================================================")