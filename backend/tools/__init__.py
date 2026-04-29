"""Tools module for Swach AI Carbon Agent"""

# Calculator Tool (Scope 1, 2, 3 calculations)
from .calculator import (
    ActivityData,
    EmissionResult,
    EmissionFactors,
    calculate_emissions,
    calculate_scope1,
    calculate_scope2,
    calculate_scope3,
    get_industry_benchmark,
    calculate_benchmark_percentile,
)

# Search Tool (Web search for carbon offsets)
from .search import (
    CarbonOffsetSearcher,
    search_carbon_offsets,
    search_ccts_information,
    search_esg_requirements,
    get_searcher,
)

# Retriever Tool (GHG Protocol knowledge base)
from .retriever import (
    GHGKnowledgeBase,
    retrieve_ghg_knowledge,
    get_knowledge_base,
)

# PDF Generator Tool (Report generation)
from .pdf_gen import (
    PDFReportGenerator,
    generate_pdf_report,
)

__all__ = [
    # Calculator
    'ActivityData',
    'EmissionResult',
    'EmissionFactors',
    'calculate_emissions',
    'calculate_scope1',
    'calculate_scope2',
    'calculate_scope3',
    'get_industry_benchmark',
    'calculate_benchmark_percentile',
    # Search
    'CarbonOffsetSearcher',
    'search_carbon_offsets',
    'search_ccts_information',
    'search_esg_requirements',
    'get_searcher',
    # Retriever
    'GHGKnowledgeBase',
    'retrieve_ghg_knowledge',
    'get_knowledge_base',
    # PDF Generator
    'PDFReportGenerator',
    'generate_pdf_report',
]
