import psycopg
from openai import OpenAI
from sentence_transformers import CrossEncoder
from step_3_rerank import connect_db, get_embedding, keyword_search, semantic_search, hybrid_search
from step_3_rerank import rerank_results

model="gpt-4.1"
openai_client = OpenAI()

def rag(question):
    # Get the initial search results
    hybrid_results = hybrid_search(question)

    # Rerank the results
    reranked_results = rerank_results(question, hybrid_results)

    # Format the final response
    information = "\n".join([f" - {title}" for title in reranked_results])

    # Send to OpenAI API for further processing
    messages = [
        {
            "role": "system",
            "content": "You are a helpful expert product recommendation assistant. Your users are asking questions about information contained in product catalogs."
            "You will be shown the user's question, and the relevant information from the product catalogs. Answer the user's question using only this information."
        },
        {"role": "user", "content": f"Question: {question}. \n Information: {information}"}
    ]

    print("Messages sent to OpenAI API:")
    # print json in pretty format
    from pprint import pprint
    import json
    # Convert to JSON string
    json_string = json.dumps(messages, indent=4)
    # Print the JSON string
    print(json_string)

    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
    return content

    return response

if __name__ == "__main__":
    # Example query
    question = "tv"

    # Get the RAG response
    rag_response = rag(question)
    print("\nRAG Response:")
    if not rag_response:
        print("No results found.")
    else:
        print(rag_response)

