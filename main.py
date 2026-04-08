import sys

# Safely swap SQLite only if we are on Render (Linux) where pysqlite3 is installed
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass # If we are on Windows, just use the standard built-in sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union, Dict, Any
from app.agents.graph import get_compiled_graph
from app.agents.state import AgentState
from fastapi.middleware.cors import CORSMiddleware 

# Initialize FastAPI
app = FastAPI(
    title="Wellness Advisor AI API",
    description="Agentic RAG backend for matching users with wellness advisors.",
    version="1.0.0"
)

# Added "*" so your upcoming Vercel frontend can connect without being blocked!
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "*" 
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize our LangGraph agent
agent_app = get_compiled_graph()

# Define the API Request Schema
class ChatRequest(BaseModel):
    user_input: str
    thread_id: str  # Critical for remembering conversation history

# Define the API Response Schema
class ChatResponse(BaseModel):
    # Updated to Union to accept BOTH simple follow-up strings and structured JSON advisor dictionaries
    response: Union[str, Dict[str, Any]] 
    is_specific_enough: bool

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Wellness Advisor AI is running."}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # 1. Define the configuration with the thread_id
        config = {"configurable": {"thread_id": request.thread_id}}
        
        # 2. Initialize the state with the user's input
        # Note: LangGraph memory will automatically append this to previous history
        initial_state = AgentState(user_input=request.user_input)
        
        # 3. Invoke the graph
        result = agent_app.invoke(initial_state, config=config)
        
        # 4. Return the response
        return ChatResponse(
            response=result["final_response"],
            is_specific_enough=result["is_specific_enough"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run the server on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)