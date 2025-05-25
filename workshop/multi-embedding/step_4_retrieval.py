from step_1_connect_db import connect_to_weaviate
from step_2_create_db import create_database, get_collection
from weaviate.classes.query import MetadataQuery
from pylate import models

# Load the ModernColBERT model
model = models.ColBERT(
    model_name_or_path="lightonai/Reason-ModernColBERT"
)

def search_documents(collection, query, reasoning=""):
    response = collection.query.near_vector(
        near_vector=model.encode(query + reasoning, is_query=True),  # Raw embedding, in [[e11, e12, e13, ...], [e21, e22, e23, ...], ...] shape
        target_vector="multi_vector",
        return_metadata=MetadataQuery(
            distance=True,
        ),
    )

    for result in response.objects:
        print(result.properties)
        print("Distance: ", result.metadata.distance)

if __name__ == "__main__":
    client = connect_to_weaviate()

    query = "At home, after I water my plants, the water goes to plates below the pots. Can I reuse it for my plants next time?"
    reasoning = """
    The user wants to know if reusing plant drainage water is safe.
    The key issue is understanding what happens to water after it passes through soil.
    It likely contains dissolved minerals and salts from fertilizers.
    We need to find information about mineral buildup, salt concentration effects on plants, and whether reused water can harm plant roots through excessive salt accumulation.
    """
    # Without reasoning, the model will not be able to provide a good answer
    search_documents(get_collection(client), query)
    client.close()