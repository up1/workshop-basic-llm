from step_1_read_pdf import read_pdf
from step_2_chunking import chunk_text
from langchain_text_splitters.sentence_transformers import SentenceTransformersTokenTextSplitter

def token_spliter(texts):
    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
    token_split_texts = []
    for text in texts:
        token_split_texts += token_splitter.split_text(text)
    return token_split_texts

if __name__ == "__main__":
    # Read the PDF file
    pdf_texts = read_pdf("./data/microsoft_annual_report_2022.pdf")
    
    # Chunk the text
    chunk_texts = chunk_text(pdf_texts)

    # Token split the text
    token_split_texts = token_spliter(chunk_texts)
    # Print the first token split
    print("First token split:")
    print(token_split_texts[0])
    print(f"\nTotal token splits: {len(token_split_texts)}")
