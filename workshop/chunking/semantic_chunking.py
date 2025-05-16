from agno.agent import Agent
from agno.document.chunking.semantic import SemanticChunking
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.chroma import ChromaDb

knowledge_base = PDFKnowledgeBase(
    path="data/ThaiRecipes.pdf",
    vector_db=ChromaDb(collection="recipes", persistent_client=True),
    chunking_strategy=SemanticChunking(similarity_threshold=0.5),
)
knowledge_base.load(recreate=False)  # Comment out after first run

agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
)

agent.print_response("How to make Som Tum?", markdown=True)