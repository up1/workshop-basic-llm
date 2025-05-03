from step_1_read_pdf import read_pdf
from step_2_chunking import chunk_text
from step_3_token_split import token_spliter

from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

def create_embedding(texts):
    """
    Create embeddings for the given texts.
    """
    embedding_function = SentenceTransformerEmbeddingFunction()
    return embedding_function(texts)


if __name__ == "__main__":
    # Read the PDF file
    pdf_texts = read_pdf("./data/microsoft_annual_report_2022.pdf")
    
    # Chunk the text
    chunk_texts = chunk_text(pdf_texts)

    # Token split the text
    token_split_texts = token_spliter(chunk_texts)
    
    # Create embeddings of first token split
    embeddings = create_embedding(token_split_texts[0])
    print("First token split:")
    print(token_split_texts[0])
    # Print the first embedding
    print("First embedding:")
    print(embeddings[0])