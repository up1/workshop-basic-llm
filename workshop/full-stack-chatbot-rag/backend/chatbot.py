"""this module contain the logic for chatbot"""

import logging
import os

from dotenv import find_dotenv, load_dotenv
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_community.document_loaders.blob_loaders import Blob
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_core.documents.base import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# setup logger object for logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load environment variables
load_dotenv(find_dotenv())
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.error("OPENAI_API_KEY is not set")
    raise ValueError("OPENAI_API_KEY is not set")

# create OpenAI instance
embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=OPENAI_API_KEY)

# setup Chroma database to store the documents
chroma = Chroma(
    collection_name="documents",
    collection_metadata={"name": "documents", "description": "store documents"},
    persist_directory="./data",
    embedding_function=embeddings,
)

# create a retriver to search the document
retriver = chroma.as_retriever(search_kwargs={"k": 2})

# create a prompt template
TEMPLATE = """
Here is the context:

<context>
{context}
</context>

And here is the question that must be answered using that context:

<question>
{input}
</question>

Please read through the provided context carefully. Then, analyze the question and attempt to find a
direct answer to the question within the context.

If you are able to find a direct answer, provide it and elaborate on relevant points from the
context using bullet points "-".

If you cannot find a direct answer based on the provided context, outline the most relevant points
that give hints to the answer of the question. For example:

If no answer or relevant points can be found, or the question is not related to the context, simply
state the following sentence without any additional text:

i couldnt find an answer did not find an answer to your question.

Output your response in plain text with Thai language without using the tags <answer> and </answer> and ensure you are not
quoting context text in your response since it must not be part of the answer.
"""

PROMPT = ChatPromptTemplate.from_template(TEMPLATE)

# create the document parsing chain to inject the document into the chatbot
llm_chain = create_stuff_documents_chain(llm, PROMPT)

# create the the retrival chain
retrival_chain = create_retrieval_chain(retriver, llm_chain)


# create function to store the document into the database
def store_document(documents: list[Document]) -> str:
    """store the document into the database
    Args:
        documents (list[dict]): list of documents to store
    """
    chroma.add_documents(documents=documents)
    return "document stored successfully"


#  create a function to retrive the document from the database
def retrieve_document(query: str) -> list[Document]:
    """retrieve the document from the database
    Args:
        query (str): query to search the document
    """
    documents = retriver.invoke(input=query)
    return documents


def ask_question(query: str) -> str:
    """chat with the chatbot
    Args:
        query (str): query to ask the chatbot
    """
    response = retrival_chain.invoke({"input": query})
    answer = response["answer"]
    return answer


# ceate a pdf parser
parser = PyPDFParser()


def parse_pdf(file_content: bytes) -> list[Document]:
    """parse the pdf file
    Args:
        file_content (bytes): content of the pdf file
    """
    blob = Blob(data=file_content)
    document = [doc for doc in parser.lazy_parse(blob)]
    return document