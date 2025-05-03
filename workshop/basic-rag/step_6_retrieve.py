import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def retrieve_from_vectordb(query):
    """
    Retrieve documents from the vector database based on the query.
    """
    # Initialize the ChromaDB client
    client = chromadb.PersistentClient(path="./db")

    # Get the collection
    embedding_function = SentenceTransformerEmbeddingFunction()
    collection = client.get_collection("microsoft_annual_report_2022", embedding_function=embedding_function)

    # Perform the query
    results = collection.query(query_texts=[query], n_results=5)

    return results['documents'][0]


if __name__ == "__main__":
    query = "Your search query here"
    retrieved_documents = retrieve_from_vectordb(query)

    for document in retrieved_documents:
        print("======================")
        print("Retrieved Document:")
        print(document)
        print('\n')