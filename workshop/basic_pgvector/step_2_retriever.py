import psycopg
import openai

# Connect to PostgreSQL database
def connect_db():
    return psycopg.connect("dbname=demo_pgvector user=user01 password=password01 host=localhost port=5432")

def get_embedding(text):
    response = openai.Client().embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

def keyword_search(query):
    sql = """
        SELECT id, title 
        FROM documents, to_tsquery('english', regexp_replace(%s, '\\s+', ' | ', 'g')) query 
        WHERE to_tsvector('english', title) @@ query 
        ORDER BY ts_rank_cd(to_tsvector('english', title), query) DESC LIMIT 5
    """
    cur.execute(sql, (query,))
    # Add distance column=0 to match the semantic search
    return [(doc_id, title, 0) for doc_id, title in cur.fetchall()]

def semantic_search(query, limit=5):
    query_embedding = get_embedding(query)
    cur.execute("""
        SELECT a.id, a.title, b.embedding <-> %s::vector AS distance
        FROM documents a
        JOIN document_embeddings b ON a.id = b.id
        ORDER BY distance ASC
        LIMIT %s
    """, (query_embedding, limit))
    return cur.fetchall()

def hybrid_search(query):
    sem_search, key_search = semantic_search(query), keyword_search(query)
    combined_search = [text for (text) in sem_search + key_search]

    # TODO Re-rank 
    
    # Merge with id
    combined_search = [(doc_id, title, distance) for doc_id, title, distance in combined_search]
    # Remove duplicates
    combined_search = list({doc_id: (doc_id, title, distance) for doc_id, title, distance in combined_search}.values())
    # Sort by distance
    combined_search.sort(key=lambda x: x[2])
    return combined_search

if __name__ == "__main__":
    # Connect to the database
    conn = connect_db()
    cur = conn.cursor()

    # Example query
    question = "sunny today"

    # 1. Keyword search example
    keyword_results = keyword_search(question)
    print("Keyword Search Results:")
    if not keyword_results:
        print("No results found.")
    else:
        for doc_id, title, distance in keyword_results:
            print(f"Document ID: {doc_id}, Title: {title}, Distance: {distance}")

    # 2. Semantic search example
    semantic_results = semantic_search(question)

    # Print results
    print("\nSemantic Search Results:")
    if not semantic_results:
        print("No results found.")
    else:
        for doc_id, title, distance in semantic_results:
            print(f"Document ID: {doc_id}, Title: {title}, Distance: {distance}")

    # 3. Hybrid search example
    hybrid_results = hybrid_search(question)
    print("\nHybrid Search Results:")
    if not hybrid_results:
        print("No results found.")
    else:
        for doc_id, title, distance in hybrid_results:
            print(f"Document ID: {doc_id}, Title: {title}, Distance: {distance}")

    # Close the cursor and connection
    cur.close()
    conn.close()
