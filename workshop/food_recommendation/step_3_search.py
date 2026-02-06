import lancedb
from lancedb.embeddings import get_registry

def get_recommendations(query):
    # Set embedding-based search openai text-embedding-3-large
    func = get_registry().get("openai").create(name="text-embedding-3-large")

    # Connect to the LanceDB database
    db = lancedb.connect("./lancedb/foods")
    table = db.open_table("food_recommendations")

    # reranker = ColbertReranker(model_name="bert-base-uncased", column="search_data")

    query_vector = func.generate_embeddings([query])[0]
    print(f"Query Vector Length: {len(query_vector)}")
    results = (
        table.search(query_type="hybrid")
        .vector(query_vector)
        .text(query)
        .limit(10)
        .to_pandas()
    )
    print(results.columns.tolist())
    if results.empty:
        print("No results found.")
        return None

    # Filter out the columns we want to display
    return results[
        ["Food_ID", "Name", "C_Type", "Veg_Non", "Rating", "_relevance_score"]
    ]


if __name__ == "__main__":
    # Search the data from vector database
    query = "pizza"
    print(f"Search Query: {query}")
    recommendations = get_recommendations(query)

    # Display the recommendations
    print("Recommendations:")
    print(recommendations)
