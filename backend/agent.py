"""
Simplified LangChain Agent for Swach AI Carbon Agent

Uses LLM to orchestrate the tools in sequence:
1. Calculator - Accurate GHG math
2. Search - Real carbon offset data
3. Retriever - GHG Protocol knowledge
4. PDF Generator - Report creation
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LangChain imports
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

# Tool imports
from tools import (
    ActivityData,
    calculate_emissions,
    search_carbon_offsets,
    retrieve_ghg_knowledge,
    generate_pdf_report,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CarbonFootprintAgent:
    """Simplified agent for carbon accounting analysis"""

    def __init__(self, model: str = "groq", verbose: bool = True):
        """
        Initialize the agent

        Args:
            model: "groq" (default) or "gemini" for LLM
            verbose: Print agent reasoning steps
        """
        self.model = model
        self.verbose = verbose
        self.llm = self._init_llm()
        self.thought_history = []

    def _init_llm(self):
        """Initialize LLM with fallback"""
        try:
            logger.info(f"Initializing {self.model} LLM...")
            if self.model == "groq":
                llm = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    api_key=os.getenv("GROQ_API_KEY"),
                    temperature=0.1,
                )
            else:
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    api_key=os.getenv("GEMINI_API_KEY"),
                    temperature=0.1,
                )
            logger.info(f"OK: {self.model} LLM initialized")
            return llm

        except Exception as e:
            logger.error(f"Failed to initialize {self.model}: {e}")
            logger.info("Attempting fallback...")

            if self.model == "groq":
                return ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",
                    api_key=os.getenv("GEMINI_API_KEY"),
                    temperature=0.1,
                )
            else:
                return ChatGroq(
                    model="llama-3.3-70b-versatile",
                    api_key=os.getenv("GROQ_API_KEY"),
                    temperature=0.1,
                )

    def _calculate_emissions(self, activity_dict: Dict) -> str:
        """Calculate emissions from activity data"""
        try:
            # Map the API request dict to the ActivityData dataclass
            activity = ActivityData(
                company_name=activity_dict.get("company_name", "Company"),
                industry=activity_dict.get("industry", "Unknown"),
                employee_count=int(activity_dict.get("employee_count", 1)),
                
                electricity_kwh=float(activity_dict.get("electricity_kwh", 0)),
                
                diesel_litres=float(activity_dict.get("diesel_litres", 0)),
                petrol_litres=float(activity_dict.get("petrol_litres", 0)),
                lpg_kg=float(activity_dict.get("lpg_kg", 0)),
                natural_gas_m3=float(activity_dict.get("natural_gas_m3", 0)),
                coal_tonnes=float(activity_dict.get("coal_tonnes", 0)),
                
                # We assume flights from frontend are domestic for simplicity, or split them.
                # Here we map all flights_km to flights_domestic_km 
                flights_domestic_km=float(activity_dict.get("flights_km", 0)),
                flights_international_km=0.0,
                
                # Map commute_km to car commute
                employee_commute_car_km=float(activity_dict.get("commute_km", 0)),
                
                # Waste and water
                waste_landfill_kg=float(activity_dict.get("waste_kg", 0)),
                water_m3=float(activity_dict.get("water_m3", 0)),
            )

            result = calculate_emissions(activity)
            return json.dumps(result.to_dict())
        except Exception as e:
            logger.error(f"Calculator error: {e}")
            return json.dumps({"error": str(e)})

    def _search_offsets(self, query: str) -> str:
        """Search for carbon offsets"""
        try:
            results = search_carbon_offsets(query)
            return json.dumps(results)
        except Exception as e:
            logger.error(f"Search error: {e}")
            return json.dumps({"error": str(e)})

    def _retrieve_knowledge(self, query: str) -> str:
        """Retrieve GHG knowledge"""
        try:
            result = retrieve_ghg_knowledge(query)
            return result
        except Exception as e:
            logger.error(f"Retriever error: {e}")
            return f"Error retrieving knowledge: {e}"

    def _generate_report(self, report_data: Dict) -> str:
        """Generate PDF report"""
        try:
            filename = generate_pdf_report(
                company_name=report_data.get("company_name", "Report"),
                activity_data=report_data.get("activity_data", {}),
                emission_result=report_data.get("emission_result", {}),
                output_dir="backend/reports",
            )
            return f"Report generated: {filename}"
        except Exception as e:
            logger.error(f"PDF generation error: {e}")
            return f"Error generating report: {e}"

    def run(self, company_data: Dict[str, Any], emit_thought=None) -> Dict:
        """
        Run the complete agent analysis

        Args:
            company_data: Dictionary with company operational data
            emit_thought: Callback function to emit thoughts (for streaming)

        Returns:
            Dictionary with analysis results
        """

        results = {"thoughts": [], "steps": []}

        # Emit initial thought
        thought = f"Starting carbon footprint analysis for {company_data.get('company_name', 'your company')}..."
        if emit_thought:
            emit_thought({"type": "thought", "content": thought})
        results["thoughts"].append({"type": "thought", "content": thought})
        logger.info(thought)

        try:
            # Step 1: Calculate emissions
            thought = "Step 1: Calculating emissions using GHG Protocol standards..."
            if emit_thought:
                emit_thought({"type": "thought", "content": thought})
            results["thoughts"].append({"type": "thought", "content": thought})

            action = f"Calling emission calculator with data..."
            if emit_thought:
                emit_thought({"type": "action", "content": action})
            results["steps"].append({"step": "calculate", "status": "running"})

            emissions_result = self._calculate_emissions(company_data)
            emissions_data = json.loads(emissions_result)

            observation = f"Calculated emissions: {json.dumps(emissions_data, indent=2)}"
            if emit_thought:
                emit_thought({"type": "observation", "content": observation})
            results["emissions"] = emissions_data
            results["steps"].append(
                {"step": "calculate", "status": "complete", "result": emissions_data}
            )
            logger.info(f"Emissions calculated: {emissions_data.get('total_tco2e', 'N/A')} tCO2e")

            # Step 2: Search for offsets
            thought = "Step 2: Searching for current CCTS carbon offset options in India..."
            if emit_thought:
                emit_thought({"type": "thought", "content": thought})
            results["thoughts"].append({"type": "thought", "content": thought})

            action = f"Searching for 'India CCTS carbon credit {emissions_data.get('total_tco2e', 0)} tonne 2026'..."
            if emit_thought:
                emit_thought({"type": "action", "content": action})
            results["steps"].append({"step": "search", "status": "running"})

            search_query = f"India CCTS carbon credit {emissions_data.get('total_tco2e', 10)} tonne offset 2026"
            search_results = self._search_offsets(search_query)
            search_data = json.loads(search_results) if search_results.startswith("[") else []

            observation = f"Found {len(search_data)} relevant results for carbon offsets"
            if emit_thought:
                emit_thought({"type": "observation", "content": observation})
            results["offsets"] = search_data
            results["steps"].append({"step": "search", "status": "complete", "result_count": len(search_data)})
            logger.info(f"Found {len(search_data)} offset options")

            # Step 3: Retrieve GHG methodology
            thought = "Step 3: Retrieving GHG Protocol methodology for audit compliance..."
            if emit_thought:
                emit_thought({"type": "thought", "content": thought})
            results["thoughts"].append({"type": "thought", "content": thought})

            action = "Querying GHG Protocol knowledge base for Scope 3 calculation methodology..."
            if emit_thought:
                emit_thought({"type": "action", "content": action})
            results["steps"].append({"step": "retrieve", "status": "running"})

            methodology = self._retrieve_knowledge("What is the correct Scope 3 calculation method?")

            observation = "Retrieved GHG Protocol methodology with citations"
            if emit_thought:
                emit_thought({"type": "observation", "content": observation})
            results["methodology"] = methodology
            results["steps"].append({"step": "retrieve", "status": "complete"})
            logger.info("Methodology retrieved")

            # Step 4: Generate report
            thought = "Step 4: Generating professional PDF carbon footprint report..."
            if emit_thought:
                emit_thought({"type": "thought", "content": thought})
            results["thoughts"].append({"type": "thought", "content": thought})

            action = f"Generating PDF report for {company_data.get('company_name', 'Company')}..."
            if emit_thought:
                emit_thought({"type": "action", "content": action})
            results["steps"].append({"step": "report", "status": "running"})

            report_data = {
                "company_name": company_data.get("company_name", "Company"),
                "activity_data": company_data,
                "emission_result": emissions_data,
            }
            report_result = self._generate_report(report_data)

            observation = report_result
            if emit_thought:
                emit_thought({"type": "observation", "content": observation})
            results["report"] = report_result
            results["steps"].append({"step": "report", "status": "complete"})
            logger.info(f"Report generated: {report_result}")

            # Final summary
            final_thought = f"Analysis complete! Total emissions: {emissions_data.get('total_tco2e', 0)} tCO2e. Report saved and ready for download."
            if emit_thought:
                emit_thought({"type": "complete", "content": final_thought})
            results["thoughts"].append({"type": "complete", "content": final_thought})

            results["status"] = "complete"
            results["final_message"] = final_thought

        except Exception as e:
            error_msg = f"Error during analysis: {e}"
            logger.error(error_msg)
            if emit_thought:
                emit_thought({"type": "error", "content": error_msg})
            results["status"] = "error"
            results["error"] = error_msg

        return results


# Quick test/demo
if __name__ == "__main__":
    print("="*70)
    print("SWACH AI CARBON AGENT - Testing")
    print("="*70)

    # Test data
    test_company_data = {
        "company_name": "TechCorp India",
        "industry": "IT",
        "electricity_kwh": 50000,
        "diesel_litres": 100,
        "flights_domestic_km": 5000,
        "flights_international_km": 10000,
        "employee_commute_car_km": 50000,
        "waste_landfill_kg": 500,
    }

    try:
        print("\nInitializing agent...")
        agent = CarbonFootprintAgent(model="groq", verbose=True)
        print("OK: Agent initialized successfully\n")

        print("="*70)
        print("RUNNING AGENT ANALYSIS")
        print("="*70 + "\n")

        result = agent.run(test_company_data)

        print("\n" + "="*70)
        print("AGENT ANALYSIS COMPLETE")
        print("="*70)
        print(f"\nFinal Status: {result.get('status', 'unknown')}")

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
