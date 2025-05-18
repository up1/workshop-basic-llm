from openai import OpenAI
from step_6_retrieve import retrieve_from_vectordb

openai_client = OpenAI()

def rag(query, retrieved_documents, model="gpt-4.1"):
    information = "\n\n".join(retrieved_documents)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful expert financial research assistant. Your users are asking questions about information contained in an annual report."
            "You will be shown the user's question, and the relevant information from the annual report. Answer the user's question using only this information."
        },
        {"role": "user", "content": f"Question: {query}. \n Information: {information}"}
    ]
    
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages,
    )
    content = response.choices[0].message.content
    return content

if __name__ == "__main__":
    query = "What was the total revenue?"

    # Retrieve documents from the database
    docs = retrieve_from_vectordb(query)
    # join the documents and distances into a single string

    print("Retrieved Documents:")
    for document, distance in zip(docs['documents'], docs['distances']):
        print("======================")
        print("Retrieved Document:")
        print(document)
        print("Distance:")
        print(distance)
        print('\n')
    
    # Use RAG to answer the question
    answer = rag(query, docs['documents'])
    print(answer)
