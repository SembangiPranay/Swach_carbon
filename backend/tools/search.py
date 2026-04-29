"""
Tavily Search Tool for Carbon Offset Research

Searches the web for real-time carbon offset options, CCTS compliance rules,
and ESG regulations in India.

This tool prevents hallucination by fetching real, current data instead of
letting the LLM make up prices or regulations.
"""

import os
from tavily import TavilyClient
from typing import List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CarbonOffsetSearcher:
    """Search for real-time carbon offset options and ESG regulations"""

    def __init__(self, api_key: str = None):
        """
        Initialize Tavily search client

        Args:
            api_key: Tavily API key (uses env var if not provided)
        """
        if api_key is None:
            api_key = os.getenv("TAVILY_API_KEY")

        if not api_key:
            raise ValueError(
                "Tavily API key not found. "
                "Set TAVILY_API_KEY environment variable or pass api_key parameter."
            )

        self.client = TavilyClient(api_key=api_key)
        logger.info("✓ Tavily client initialized")

    def search_carbon_offsets(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for carbon offset information

        Args:
            query: Search query (e.g., "India CCTS carbon credit price 2026")
            max_results: Maximum number of results to return

        Returns:
            List of search results with title, snippet, link, source
        """
        logger.info(f"Searching: {query}")

        try:
            response = self.client.search(
                query,
                search_depth="advanced",
                max_results=max_results,
                include_answer=True
            )

            results = []
            for result in response.get("results", []):
                formatted_result = {
                    'title': result.get('title', 'No title'),
                    'snippet': result.get('content', '')[:300],  # First 300 chars
                    'link': result.get('url', ''),
                    'source': result.get('source', 'Unknown'),
                    'score': result.get('score', 0),
                }
                results.append(formatted_result)

            logger.info(f"✓ Found {len(results)} results")
            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    def search_ccts_offsets(self) -> List[Dict[str, Any]]:
        """Search for CCTS-approved carbon offset projects"""
        query = "India CCTS carbon credit trading scheme registered projects 2026 price"
        return self.search_carbon_offsets(query, max_results=5)

    def search_renewable_energy_offsets(self) -> List[Dict[str, Any]]:
        """Search for renewable energy based carbon offsets"""
        query = "India renewable energy carbon offset projects 2026"
        return self.search_carbon_offsets(query, max_results=5)

    def search_esg_compliance(self, industry: str = None) -> List[Dict[str, Any]]:
        """Search for ESG compliance requirements"""
        if industry:
            query = f"India ESG compliance requirements {industry} 2026 carbon reporting"
        else:
            query = "India ESG compliance carbon reporting requirements 2026"
        return self.search_carbon_offsets(query, max_results=5)

    def search_emission_reduction_strategies(self, emission_type: str) -> List[Dict[str, Any]]:
        """Search for strategies to reduce specific emission types"""
        queries = {
            'electricity': 'India renewable energy options reduce electricity emissions 2026',
            'travel': 'India sustainable travel options reduce flight emissions carbon offset',
            'waste': 'India waste management circular economy carbon reduction',
            'supply_chain': 'India supply chain decarbonization sustainable suppliers',
        }

        query = queries.get(emission_type, f"India reduce {emission_type} emissions 2026")
        return self.search_carbon_offsets(query, max_results=5)

    def format_results_for_llm(self, results: List[Dict[str, Any]]) -> str:
        """
        Format search results for LLM consumption

        Args:
            results: List of search results

        Returns:
            Formatted string for agent to read
        """
        if not results:
            return "No results found."

        formatted = "Search Results:\n\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   Source: {result['source']}\n"
            formatted += f"   Summary: {result['snippet']}\n"
            formatted += f"   Link: {result['link']}\n\n"

        return formatted


# Singleton instance for use in agent
_searcher = None


def get_searcher() -> CarbonOffsetSearcher:
    """Get or create singleton searcher instance"""
    global _searcher
    if _searcher is None:
        _searcher = CarbonOffsetSearcher()
    return _searcher


def search_carbon_offsets(query: str) -> str:
    """
    Tool function for LangChain agent

    Args:
        query: Search query

    Returns:
        Formatted string with search results
    """
    searcher = get_searcher()
    results = searcher.search_carbon_offsets(query, max_results=5)
    return searcher.format_results_for_llm(results)


def search_ccts_information() -> str:
    """Tool function: Search CCTS information"""
    searcher = get_searcher()
    results = searcher.search_ccts_offsets()
    return searcher.format_results_for_llm(results)


def search_esg_requirements(industry: str = None) -> str:
    """Tool function: Search ESG requirements"""
    searcher = get_searcher()
    results = searcher.search_esg_compliance(industry)
    return searcher.format_results_for_llm(results)


# Example usage
if __name__ == "__main__":
    searcher = CarbonOffsetSearcher()

    print("\n" + "="*60)
    print("TEST 1: Search for CCTS offsets")
    print("="*60)
    results = searcher.search_ccts_offsets()
    print(searcher.format_results_for_llm(results))

    print("\n" + "="*60)
    print("TEST 2: Search for ESG compliance")
    print("="*60)
    results = searcher.search_esg_compliance("IT")
    print(searcher.format_results_for_llm(results))

    print("\n" + "="*60)
    print("TEST 3: Search for emission reduction (electricity)")
    print("="*60)
    results = searcher.search_emission_reduction_strategies("electricity")
    print(searcher.format_results_for_llm(results))

    print("\n✓ All searches completed successfully!")
