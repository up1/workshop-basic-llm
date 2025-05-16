import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
import umap
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

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
        results = collection.query(query_texts=query, n_results=5, include=['documents', 'embeddings'])

        # Get the embeddings for the entire collection
        embeddings = collection.get(include=['embeddings'])['embeddings']
        query_embedding = embedding_function([query])[0]
        retrieved_embeddings = results['embeddings'][0]

        # Set up UMAP for dimensionality reduction
        umap_transform = umap.UMAP(random_state=0, transform_seed=0).fit(embeddings)
        projected_dataset_embeddings = project_embeddings(embeddings, umap_transform)
        projected_query_embedding = project_embeddings([query_embedding], umap_transform)
        projected_retrieved_embeddings = project_embeddings(retrieved_embeddings, umap_transform)

        # Visualize the results
        visualize_results(projected_dataset_embeddings, projected_query_embedding, projected_retrieved_embeddings)

        return results['documents'][0]
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)

def project_embeddings(embeddings, umap_transform):
    umap_embeddings = np.empty((len(embeddings),2))
    for i, embedding in enumerate(tqdm(embeddings)): 
        umap_embeddings[i] = umap_transform.transform([embedding])
    return umap_embeddings
    
def visualize_results(projected_dataset_embeddings, projected_query_embedding, projected_retrieved_embeddings):
    plt.figure()
    plt.scatter(projected_dataset_embeddings[:, 0], projected_dataset_embeddings[:, 1], s=10, color='gray')
    plt.scatter(projected_query_embedding[:, 0], projected_query_embedding[:, 1], s=150, marker='X', color='r')
    plt.scatter(projected_retrieved_embeddings[:, 0], projected_retrieved_embeddings[:, 1], s=100, facecolors='none', edgecolors='g')

    plt.gca().set_aspect('equal', 'datalim')
    plt.title(f'{query}')
    plt.axis('off')
    plt.show()
    print("Visualizing results...")

if __name__ == "__main__":
    query = "What was the total revenue?"
    results = retrieve_from_vectordb(query)
    for result in results:
        print("======================")
        print("Retrieved Document:")
        print(result)
        print('\n')