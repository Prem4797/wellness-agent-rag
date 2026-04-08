import json
import os
import shutil
from dotenv import load_dotenv

from langchain_chroma import Chroma 
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings 
from tqdm import tqdm 

load_dotenv()

# Centralize the embedding model
def get_embedding_model():
    return HuggingFaceEmbeddings(model_name="BAAI/bge-base-en-v1.5")

def index_advisors(file_path: str, batch_size: int = 32):
    embeddings = get_embedding_model()
    documents = []
    
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return

    print("Loading and mapping documents from JSONL...")
    with open(file_path, 'r', encoding='utf-8') as f:
        # Using enumerate to track line numbers for error reporting
        for line_number, line in enumerate(f, start=1):
            
            # 1. ROBUST READING: Skip completely blank lines
            if not line.strip():
                continue
            
            # 2. ROBUST READING: Safely try to parse the JSON
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                print(f"Skipping Line {line_number}: Invalid JSON format.")
                continue
            
            # 3. SAFETY TRUNCATION: Ensure the bio doesn't blow past the 512 token limit
            bio = data.get("bio", "")
            bio_words = bio.split()
            if len(bio_words) > 250:
                bio = " ".join(bio_words[:250]) + "... [Bio truncated for length]"

            # 4. SEMANTIC TEXT (Page Content): Formatted like a resume for the LLM
            rich_content = (
                f"Name: {data.get('name', 'Unknown')}\n"
                f"Credentials: {data.get('credentials', 'Not specified')}\n"
                f"Specializations: {', '.join(data.get('specializations', []))}\n"
                f"Focus Areas: {', '.join(data.get('focus_areas', []))}\n"
                f"Bio: {bio}\n"
                f"Treatment Approach: {data.get('approach', 'Not specified')}"
            )
            
            # 5. HARD METADATA: Stored strictly for database filtering
            # Standardizing lists to strings for ChromaDB compatibility
            metadata = {
                "advisor_id": data.get("advisor_id", "unknown"),
                "languages": ", ".join(data.get("languages", ["English"])),
                "availability": ", ".join(data.get("availability", ["unknown"])) if isinstance(data.get("availability"), list) else data.get("availability", "unknown"),
                "session_type": ", ".join(data.get("session_type", ["unknown"])),
                "rating": float(data.get("rating", 0.0)),
                "price_range": data.get("price_range", "unknown"),
                "location": data.get("location", "unknown"),
                "experience_years": int(data.get("experience_years", 0))
            }
            
            documents.append(Document(
                page_content=rich_content,
                metadata=metadata
            ))

    print(f"Successfully mapped {len(documents)} intact advisor profiles.")

    # Clean slate to prevent dimension mismatches or duplicates
    if os.path.exists("./chroma_db"):
        print("Cleaning up old database for a fresh start...")
        shutil.rmtree("./chroma_db")

    # Initialize Store
    vectorstore = Chroma(
        persist_directory="./chroma_db", 
        embedding_function=embeddings
    )

    print(f"\nStarting local indexing in safe batches of {batch_size}...")

    # Batch processing to prevent Out-Of-Memory (OOM) errors and SQLite limits
    for i in tqdm(range(0, len(documents), batch_size), desc="Embedding Batches"):
        batch = documents[i : i + batch_size]
        vectorstore.add_documents(batch)

    print("\nSuccess! Entity-based Knowledge Base rebuilt in ./chroma_db")

def get_vectorstore():
    """Connects to the existing ChromaDB for querying."""
    embeddings = get_embedding_model()
    return Chroma(
        persist_directory="./chroma_db", 
        embedding_function=embeddings
    )

if __name__ == "__main__":
    # Entry Point
    index_advisors("app/data/advisors.jsonl")