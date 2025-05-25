from weaviate.classes.config import Configure, Property, DataType
from weaviate.util import generate_uuid5
from weaviate.classes.config import Configure
import json
from step_1_connect_db import connect_to_weaviate

collection_name = "DemoCollection"

def create_database(client):
    # Check if collection exists before deleting
    if client.collections.exists(collection_name):
        client.collections.delete(collection_name)

    client.collections.create(
        collection_name,
        vectorizer_config=[
            # User-provided embeddings
            Configure.NamedVectors.none(
                name="multi_vector",
                vector_index_config=Configure.VectorIndex.hnsw(
                    # Enable multi-vector index with default settings
                    multi_vector=Configure.VectorIndex.MultiVector.multi_vector()
                )
            ),
        ],
        properties=[
            Property(name="text",
                    data_type=DataType.TEXT,
                    vectorize_property_name=False  # Explicitly disable property name vectorization
                    ),
            Property(name="docid",
                    data_type=DataType.TEXT,
                    vectorize_property_name=False  # Explicitly disable property name vectorization
                    ),
        ],
    )
    print(f"Collection '{collection_name}' created successfully.")

def get_collection(client):
    # Get collection
    if not client.collections.exists(collection_name):
        raise ValueError(f"Collection '{collection_name}' does not exist.")
    return client.collections.get(collection_name)

def print_collection_info(client):
    # Get collection
    collection = get_collection(client)
    config = collection.config.get().vector_config['multi_vector'].vector_index_config
    print(json.dumps(config.__dict__, indent=2, default=lambda o: o.__dict__ if hasattr(o, '__dict__') else str(o)))





if __name__ == "__main__":
    client = connect_to_weaviate()
    create_database(client)
    print_collection_info(client)
    client.close()