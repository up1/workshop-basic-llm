from step_1_read_pdf import read_pdf
from helper_utils import word_wrap
from langchain.text_splitter import RecursiveCharacterTextSplitter


def chunk_text(texts):
    character_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=1000,
        chunk_overlap=0
        )
    character_split_texts = character_splitter.split_text('\n\n'.join(texts))
    return character_split_texts

if __name__ == "__main__":
    # Read the PDF file
    pdf_texts = read_pdf("./data/microsoft_annual_report_2022.pdf")
    
    # Chunk the text
    chunk_texts = chunk_text(pdf_texts)
    # Print the first chunk
    print("First chunk:")
    print(chunk_texts[0])
    print(f"\nTotal chunks: {len(chunk_texts)}")