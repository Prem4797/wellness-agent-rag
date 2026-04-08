=================== ASYNCHRONOUS DATA PIPELINE ===================
[JSONL Data] ──> (Chunking/Formatting) ──> [ ENCODER: Gemini-Embedding-001 ] ──> [( ChromaDB )]
                                                                                     ▲
=================== REAL-TIME INFERENCE PIPELINE ===================                 │
                                                                                     │
[ User Request via FastAPI ]                                                         │
       │                                                                             │
       ▼                                                                             │
[ CHECKPOINTER / MEMORY LAYER ] (Loads previous chat history via Thread ID)          │
       │                                                                             │
       ▼                                                                             │
( Pydantic AgentState ) <─────────────────────────────────┐                          │
       │                                                  │                          │
       ▼                                                  │                          │
 ┌─────────────────────────────┐                          │                          │
 │ NODE 1: Intake / Router     │ ── (Vague) ──────────────┤                          │
 └─────────────────────────────┘                          │                          │
       │                                                  │                          │
    (Specific: Extracts Topic & Metadata)                 │                          │
       │                                                  │                          │
       ▼                                                  │                          │
 ┌─────────────────────────────┐                          │                          │
 │ NODE 2: Retrieval Agent     │                          │                          │
 │  ├── 1. Metadata Filter     │                          │                          │
 │  ├── 2. [ ENCODER Model ]   │ ──(Vector Match)─────────┴──────────────────────────┘
 │  └── 3. Semantic Search     │ 
 └─────────────────────────────┘
       │
    (Returns Top 3 Matches)
       │
       ▼
 ┌─────────────────────────────┐
 │ NODE 3: Synthesizer Agent   │ 
 │ (Guardrails & Formatting)   │
 └─────────────────────────────┘
       │
       ▼
[ Final Empathetic Response ] ──> [ CHECKPOINTER ] (Saves new state) ──> [ User ]

=================== ASYNCHRONOUS MLOps & EVALUATION ===================
       ▲
       │ (Streams all execution traces, latency, and token usage in background)
       ▼
[ TELEMETRY: LangSmith / DataDog ] ──> [ EVALUATION: RAGAS Framework ]
                                       (Calculates NDCG@k, Context Precision, Answer Relevance)