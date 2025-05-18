import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from sentence_transformers import CrossEncoder

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
        results = collection.query(query_texts=[query], n_results=3, include=["documents", "metadatas", "distances"])
        retrieved_documents = results['documents'][0]
        print("Retrieved documents:")
        for doc in retrieved_documents:
            print(doc)
            print('\n')

        # Rerank the results using a CrossEncoder
        cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-12-v2')

        # Re-rank and return the results
        reranked_results = cross_encoder.predict([(query, doc) for doc in retrieved_documents], show_progress_bar=True)

        # Merge results['documents'][0] with results['distances'][0]
        merged_results = {
            "documents": retrieved_documents,
            "reranked_scores": reranked_results
        }
        # Sort the merged results based on reranked scores
        sorted_indices = reranked_results.argsort()[::-1]
        merged_results["documents"] = [merged_results["documents"][i] for i in sorted_indices]
        merged_results["reranked_scores"] = [merged_results["reranked_scores"][i] for i in sorted_indices]

        return merged_results
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)


if __name__ == "__main__":
    query = "What was the total revenue?"
    results = retrieve_from_vectordb(query)
    for result in results['documents']:
        print("======================")
        print("Reranked Result:")
        print(result)
        print('\n')