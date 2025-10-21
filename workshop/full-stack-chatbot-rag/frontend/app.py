"""this web application build t using streamlit"""

import streamlit as st
import requests


# define the logic for the application
def ask(query: str) -> str:
    """ask the chatbot a question
    Args:
        query (str): question to ask the chatbot
    return:
        str: answer from the chatbot
    """
    with st.spinner("Asking the chatbot..."):
        response = requests.get(f"{API_URL}/ask?query={query}")

    if response.status_code == 200:
        data = response.json()
        return data["answer"]
    else:
        return "I couldn't find an answer to your question."


# define the base url for the API
API_URL = "http://localhost:8000"  # change this to the deployed API URL
st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("Chatbot RAG")

uploaded_files = st.file_uploader(
    "Upload you pdf docs", type="pdf", accept_multiple_files=True
)
if uploaded_files:
    files = [
        ("files", (file.name, file.getvalue(), "application/pdf"))
        for file in uploaded_files
    ]
    try:
        with st.spinner("Uploading files..."):
            response = requests.post(f"{API_URL}/documents/", files=files)
        if response.status_code == 200:
            st.success("Files uploaded successfully")
            uploaded_files = None
        else:
            st.error("Failed to upload files")
    except Exception as e:
        st.error(f"Error uploading files: {e}")


with st.chat_message(name="ai", avatar="ai"):
    st.write("Hello! I'm the Chatbot RAG. How can I help you today?")

query = st.chat_input(placeholder="Type your question here...")

if query:
    with st.chat_message("user"):
        st.write(query)
    answer = ask(query)
    with st.chat_message("ai"):
        st.write(answer)