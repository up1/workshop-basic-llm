from pypdf import PdfReader


def read_pdf(file_path):
    """Read a PDF file and return its text content."""
    reader = PdfReader(file_path)
    pdf_texts = [p.extract_text().strip() for p in reader.pages]

    # Filter the empty strings
    pdf_texts = [text for text in pdf_texts if text]
    
    return pdf_texts

if __name__ == "__main__":
    texts = read_pdf("./data/microsoft_annual_report_2022.pdf")
    # Print the first text
    print(texts[0])
    
