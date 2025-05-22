import psycopg
import openai

# Connect to PostgreSQL database
def connect_db():
    return psycopg.connect("dbname=demo_pgvector user=user01 password=password01 host=localhost port=5432")

def get_embedding(text):
    response = openai.Client().embeddings.create(input=text, model="text-embedding-ada-002")
    return response.data[0].embedding

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

if __name__ == "__main__":
    # Connect to the database
    conn = connect_db()
    cur = conn.cursor()

    # Example query
    question = "sunny"
    results = semantic_search(question)

    # Print results
    for doc_id, title, distance in results:
        print(f"Document ID: {doc_id}, Title: {title}, Distance: {distance}")
    cur.close()
    conn.close()
