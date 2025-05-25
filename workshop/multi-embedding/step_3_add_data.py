from step_1_connect_db import connect_to_weaviate
from step_2_create_db import create_database, get_collection
from weaviate.util import generate_uuid5
from pylate import models

# Load the ModernColBERT model
model = models.ColBERT(
    model_name_or_path="lightonai/Reason-ModernColBERT"
)

relevant_document = """
**Soluble Salts in Container Plants**

Soluble salts are minerals dissolved in water that accumulate when water evaporates, leaving salts behind.
When drainage water is reused, these salts become concentrated and make it difficult for plants to absorb water.
High salt levels can damage roots directly and cause symptoms like brown leaf tips, wilting, and stunted growth.
The best practice is to empty drainage saucers rather than reusing the water.
"""

irrelevant_document = """
**Water Conservation in Gardening**

Water conservation is important for sustainable gardening.
Techniques include mulching to reduce evaporation, choosing drought-tolerant plants, and collecting rainwater in barrels.
Drip irrigation systems deliver water directly to plant roots with minimal waste.
These methods can reduce garden water usage by up to 50% while maintaining healthy plants.
"""

somewhat_related_document = """
**Basic Plant Watering Guidelines**

Most houseplants should be watered when the top inch of soil feels dry.
Water thoroughly until it drains from the bottom holes, then empty saucers after 30 minutes to prevent root rot.
Different plants have different needs - succulents need less water while tropical plants prefer consistently moist soil.
Overwatering causes more plant deaths than underwatering.
"""

def add_data(collection):
    # An example dataset
    documents = [
        {"id": "doc1", "text": relevant_document},
        {"id": "doc2", "text": irrelevant_document},
        {"id": "doc3", "text": somewhat_related_document},
    ]

    # Import data
    with collection.batch.fixed_size(batch_size=10) as batch:
        for doc in documents:
            # Iterate through the dataset & add to batch
            batch.add_object(
                properties={"text": doc["text"], "docid": doc["id"]},
                uuid=generate_uuid5(doc["id"]),
                vector={"multi_vector": model.encode(doc["text"], is_query=False)},  # Provide the embedding manually
            )

def fetch_data(collection):
    response = collection.query.fetch_objects(limit=3, include_vector=True)
    for obj in response.objects:
        print(obj.properties['docid'])
        print(f"This embedding's shape is ({len(obj.vector['multi_vector'])}, {len(obj.vector['multi_vector'][0])})")


if __name__ == "__main__":
    client = connect_to_weaviate()
    create_database(client)
    add_data(get_collection(client))
    fetch_data(get_collection(client))
    client.close()