"""
ChromaDB Retriever for GHG Protocol Knowledge Base

Stores GHG Protocol PDFs as searchable embeddings to prevent LLM hallucination.
When the agent needs to cite methodology or explain a calculation, it retrieves
accurate information from the knowledge base instead of making something up.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

try:
    from langchain_community.document_loaders.pdf import PyPDFLoader as PDFLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import Chroma
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    import sys
    print(f"WARNING: LangChain components not fully installed")
    print(f"Run: pip install pypdf langchain-community")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GHGKnowledgeBase:
    """
    Vector database of GHG Protocol and carbon accounting knowledge

    Usage:
        kb = GHGKnowledgeBase()
        kb.setup()  # One-time setup - downloads and processes PDFs
        results = kb.retrieve("Scope 3 calculation method")
    """

    def __init__(self, db_path: str = "backend/data/chroma_db"):
        """
        Initialize knowledge base

        Args:
            db_path: Path where ChromaDB vector store is persisted
        """
        self.db_path = db_path
        self.vectorstore = None
        self.embeddings = None
        logger.info(f"Knowledge base path: {db_path}")

    def _initialize_embeddings(self):
        """Initialize the embedding model"""
        if self.embeddings is None:
            logger.info("Initializing embeddings (this may take a moment)...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={"device": "cpu"}  # Use CPU for compatibility
            )
            logger.info("✓ Embeddings initialized")

    def _load_vectorstore(self):
        """Load existing vector store from disk"""
        if self.vectorstore is None:
            self._initialize_embeddings()
            try:
                self.vectorstore = Chroma(
                    persist_directory=self.db_path,
                    embedding_function=self.embeddings,
                    collection_name="ghg_protocol"
                )
                logger.info(f"✓ Loaded existing vector store from {self.db_path}")
            except Exception as e:
                logger.warning(f"Could not load vector store: {e}")
                return False
        return True

    def setup(self, pdf_paths: List[str] = None):
        """
        Setup knowledge base by processing PDFs and storing embeddings

        Args:
            pdf_paths: List of PDF file paths to load
                      If None, looks for PDFs in backend/data/
        """
        logger.info("Setting up knowledge base...")

        # Find PDFs if not specified
        if pdf_paths is None:
            data_dir = Path("backend/data")
            pdf_paths = list(data_dir.glob("*.pdf"))

            if not pdf_paths:
                logger.warning(
                    "No PDFs found in backend/data/. "
                    "Please download GHG Protocol PDFs from ghgprotocol.org"
                )
                return False

        logger.info(f"Found {len(pdf_paths)} PDFs to process")

        # Initialize embeddings
        self._initialize_embeddings()

        # Load and process documents
        all_documents = []
        for pdf_path in pdf_paths:
            logger.info(f"Loading {pdf_path}...")
            try:
                loader = PDFLoader(str(pdf_path))
                documents = loader.load()
                all_documents.extend(documents)
                logger.info(f"  ✓ Loaded {len(documents)} pages")
            except Exception as e:
                logger.error(f"  ✗ Error loading {pdf_path}: {e}")

        if not all_documents:
            logger.error("No documents loaded from PDFs")
            return False

        logger.info(f"Total documents loaded: {len(all_documents)}")

        # Split into chunks
        logger.info("Splitting documents into chunks...")
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        chunks = splitter.split_documents(all_documents)
        logger.info(f"Created {len(chunks)} chunks")

        # Create vector store
        logger.info("Creating embeddings and vector store...")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.db_path,
            collection_name="ghg_protocol"
        )
        logger.info(f"✓ Vector store created and persisted to {self.db_path}")

        return True

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents from knowledge base

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant document chunks with metadata
        """
        if not self._load_vectorstore():
            logger.error("Vector store not available")
            return []

        try:
            logger.info(f"Retrieving documents for: {query}")
            results = self.vectorstore.similarity_search(query, k=k)

            formatted_results = []
            for i, doc in enumerate(results, 1):
                formatted_results.append({
                    'rank': i,
                    'content': doc.page_content,
                    'source': doc.metadata.get('source', 'Unknown'),
                    'page': doc.metadata.get('page', 'Unknown'),
                })

            logger.info(f"✓ Retrieved {len(formatted_results)} relevant documents")
            return formatted_results

        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            return []

    def retrieve_formatted(self, query: str, k: int = 3) -> str:
        """
        Retrieve and format results as string for LLM

        Args:
            query: Search query
            k: Number of results

        Returns:
            Formatted string ready for LLM consumption
        """
        results = self.retrieve(query, k=k)

        if not results:
            return "No relevant information found in knowledge base."

        formatted = f"GHG Protocol Knowledge Base Results:\n\n"
        for result in results:
            formatted += f"[Source: {result['source']}, Page {result['page']}]\n"
            formatted += f"{result['content']}\n\n"

        return formatted

    def get_scope1_methodology(self) -> str:
        """Get Scope 1 calculation methodology"""
        return self.retrieve_formatted(
            "Scope 1 direct emissions fuel combustion calculation method"
        )

    def get_scope2_methodology(self) -> str:
        """Get Scope 2 calculation methodology"""
        return self.retrieve_formatted(
            "Scope 2 purchased electricity emission factors grid"
        )

    def get_scope3_methodology(self) -> str:
        """Get Scope 3 calculation methodology"""
        return self.retrieve_formatted(
            "Scope 3 indirect value chain employee business travel waste"
        )

    def get_emission_factors(self) -> str:
        """Get emission factors and standards"""
        return self.retrieve_formatted(
            "emission factors DEFRA IPCC CO2 diesel electricity"
        )

    def get_compliance_requirements(self) -> str:
        """Get GHG Protocol compliance requirements"""
        return self.retrieve_formatted(
            "GHG Protocol compliance requirements audit boundary"
        )


# Singleton instance for use in agent
_knowledge_base = None


def get_knowledge_base() -> GHGKnowledgeBase:
    """Get or create singleton knowledge base instance"""
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = GHGKnowledgeBase()
    return _knowledge_base


def retrieve_ghg_knowledge(query: str, k: int = 3) -> str:
    """
    Tool function for LangChain agent

    Args:
        query: Search query
        k: Number of results

    Returns:
        Formatted string with retrieval results
    """
    kb = get_knowledge_base()
    return kb.retrieve_formatted(query, k=k)


# Example usage and testing
if __name__ == "__main__":
    kb = GHGKnowledgeBase()

    print("\n" + "="*60)
    print("GHG PROTOCOL KNOWLEDGE BASE SETUP")
    print("="*60)

    # Check if PDFs exist
    pdf_dir = Path("backend/data")
    pdfs = list(pdf_dir.glob("*.pdf"))

    if not pdfs:
        print("\n⚠️  No PDFs found in backend/data/")
        print("\nTo use this tool, download GHG Protocol documents from:")
        print("  https://ghgprotocol.org/")
        print("\nPlace PDF files in: backend/data/")
        print("\nSuggested files to download:")
        print("  - GHG Protocol Corporate Standard.pdf")
        print("  - Scope 3 Calculation Guidance.pdf")
    else:
        print(f"\nFound {len(pdfs)} PDF files:")
        for pdf in pdfs:
            print(f"  - {pdf.name}")

        print("\nSetting up knowledge base...")
        success = kb.setup(pdf_paths=pdfs)

        if success:
            print("\n" + "="*60)
            print("RETRIEVAL TESTS")
            print("="*60)

            print("\nTest 1: Scope 1 methodology")
            print(kb.retrieve_formatted("Scope 1 direct emissions calculation"))

            print("\nTest 2: Scope 3 methodology")
            print(kb.retrieve_formatted("Scope 3 business travel flights"))

            print("\n✓ Knowledge base ready!")
        else:
            print("\n✗ Setup failed - PDF processing error")
