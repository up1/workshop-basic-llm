import lancedb
from lancedb.rerankers import ColbertReranker

def get_recommendations(query):
    # Connect to the LanceDB database
    db = lancedb.connect("./lancedb/foods")
    table = db.open_table("food_recommendations")

    # Create a reranker for hybrid search
    reranker = ColbertReranker(column="search_data", query=query, k=10)

    results = (
        table.search(
            query, 
            query_type="hybrid",
            vector_column_name="vector",
            fts_columns="search_data"
        )
        .rerank(reranker)
        .limit(10)
        .to_pandas()
    )
    if results.empty:
        print("No results found.")
        return None

    # Filter out the columns we want to display
    return results[["Food_ID", "Name", "C_Type", "Veg_Non", "Rating", "_relevance_score"]]


if __name__ == "__main__":
    # Search the data from vector database
    query = "pizza"
    print(f"Search Query: {query}")
    recommendations = get_recommendations(query)
    
    # Display the recommendations
    print("Recommendations:")
    print(recommendations)