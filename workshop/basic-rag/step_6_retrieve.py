import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def retrieve_from_vectordb(query):
    """
    Retrieve documents from the vector database based on the query.
    """
    try:
        # Initialize the ChromaDB client
        client = chromadb.PersistentClient(path="./db")

        # Get the collection
        embedding_function = SentenceTransformerEmbeddingFunction()
        collection = client.get_collection("microsoft_annual_report_2022", embedding_function=embedding_function)

        # query with scores and sort by distance
        results = collection.query(query_texts=[query], n_results=5, include=["documents", "metadatas", "distances"])

        # Merge results['documents'][0] with results['distances'][0]
        merged_results = {
            "documents": results['documents'][0],
            "distances": results['distances'][0]
        }

        return merged_results
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    query = "What was the total revenue?"
    results = retrieve_from_vectordb(query)

    for document, distance in zip(results['documents'], results['distances']):
        print("======================")
        print("Retrieved Document:")
        print(document)
        print("Distance:")
        print(distance)
        print('\n')