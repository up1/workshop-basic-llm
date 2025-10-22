import asyncio
from agno.agent import Agent
from agno.knowledge.chunking.document import DocumentChunking
from agno.knowledge.knowledge import Knowledge
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.vectordb.chroma import ChromaDb

knowledge_base = Knowledge(
    vector_db=ChromaDb(collection="recipes", persistent_client=True)
)

asyncio.run(knowledge_base.add_content_async(
    path="data/microsoft_annual_report_2022.pdf",
    reader=PDFReader(
        name="Document Chunking Reader",
        chunking_strategy=DocumentChunking(),
    )
))

agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
)

agent.print_response("What was the total revenue of microsoft?", markdown=True)
