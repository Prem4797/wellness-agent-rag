from pydantic import BaseModel, Field
from typing import List, Annotated, Optional, Dict, Any, Union
import operator

class AgentState(BaseModel):
    # 1. Inputs & Memory
    user_input: str = Field(default="")
    chat_history: Annotated[List[Dict[str, str]], operator.add] = Field(default_factory=list)
    
    # 2. Intake / Router Outputs
    is_specific_enough: bool = Field(default=False)
    extracted_topic: Optional[str] = Field(default=None)
    extracted_filters: Dict[str, Any] = Field(default_factory=dict)
    
    # 3. Retrieval Outputs
    retrieved_advisors: List[Dict[str, Any]] = Field(default_factory=list)
    
    # 4. Final System Output
    # Updated to Union to accept both strings (Intake follow-ups) and dicts (Synthesizer JSON)
    final_response: Union[str, Dict[str, Any]] = Field(default="")