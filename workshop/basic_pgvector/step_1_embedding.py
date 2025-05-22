import openai
import psycopg

model_id = "text-embedding-ada-002"

# Connect to PostgreSQL database
conn = psycopg.connect("dbname=demo_pgvector user=user01 password=password01 host=localhost port=5432")

# Fetch documents from the database
cur = conn.cursor()
cur.execute("SELECT id, title FROM documents")
documents = cur.fetchall()

# Process and store embeddings in the database
for doc_id, doc_title in documents:
    embedding = openai.embeddings.create(
        input=doc_title, 
        model=model_id).data[0].embedding
    cur.execute("INSERT INTO document_embeddings (id, embedding) VALUES (%s, %s);", (doc_id, embedding))
    conn.commit()

# Commit and close the database connection
conn.commit()
cur.close()