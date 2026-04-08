from app.utils.vectorstore import get_vectorstore

def verify_database():
    vectorstore = get_vectorstore()
    
    # 1. Check the total count of items in the collection
    collection_count = vectorstore._collection.count()
    print(f"Total documents in ChromaDB: {collection_count}")

    # 2. Perform a sample similarity search
    query = "I am looking for an advisor who helps with stress and trauma"
    results = vectorstore.similarity_search(query, k=2)

    print("\n--- Sample Search Results ---")
    for doc in results:
        print(f"ID: {doc.metadata.get('advisor_id')}")
        print(f"Content: {doc.page_content[:150]}...")
        print("-" * 30)

if __name__ == "__main__":
    verify_database()