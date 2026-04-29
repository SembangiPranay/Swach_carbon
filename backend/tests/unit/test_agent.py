import pytest
from unittest.mock import patch, MagicMock
from agent import CarbonFootprintAgent
import json

class TestCarbonFootprintAgent:
    
    @patch('agent.ChatGroq')
    @patch('agent.ChatGoogleGenerativeAI')
    def test_init_groq_success(self, mock_gemini, mock_groq):
        agent = CarbonFootprintAgent(model="groq", verbose=False)
        assert agent.model == "groq"
        assert agent.verbose == False
        mock_groq.assert_called_once()
        
    @patch('agent.ChatGroq')
    @patch('agent.ChatGoogleGenerativeAI')
    def test_init_gemini_success(self, mock_gemini, mock_groq):
        agent = CarbonFootprintAgent(model="gemini", verbose=False)
        assert agent.model == "gemini"
        mock_gemini.assert_called_once()

    @patch('agent.ChatGroq', side_effect=Exception("API Error"))
    @patch('agent.ChatGoogleGenerativeAI')
    def test_init_fallback_to_gemini(self, mock_gemini, mock_groq):
        agent = CarbonFootprintAgent(model="groq", verbose=False)
        assert mock_groq.call_count == 1
        assert mock_gemini.call_count == 1
        
    @patch('agent.calculate_emissions')
    def test_calculate_emissions(self, mock_calculate):
        mock_result = MagicMock()
        mock_result.to_dict.return_value = {"total_tco2e": 500.5}
        mock_calculate.return_value = mock_result
        
        agent = CarbonFootprintAgent(model="mock")
        
        test_data = {
            "company_name": "Test Co",
            "electricity_kwh": 1000,
            "diesel_litres": 50
        }
        
        result_json = agent._calculate_emissions(test_data)
        result_dict = json.loads(result_json)
        
        assert result_dict["total_tco2e"] == 500.5
        mock_calculate.assert_called_once()
        
        # Verify the ActivityData object constructed
        activity_arg = mock_calculate.call_args[0][0]
        assert activity_arg.company_name == "Test Co"
        assert activity_arg.electricity_kwh == 1000
        assert activity_arg.diesel_litres == 50
        
    @patch('agent.search_carbon_offsets')
    def test_search_offsets(self, mock_search):
        mock_search.return_value = [{"title": "Offset project", "link": "url"}]
        agent = CarbonFootprintAgent(model="mock")
        
        result = agent._search_offsets("query")
        assert "Offset project" in result
        
    @patch('agent.CarbonFootprintAgent._calculate_emissions')
    @patch('agent.CarbonFootprintAgent._search_offsets')
    @patch('agent.CarbonFootprintAgent._retrieve_knowledge')
    @patch('agent.CarbonFootprintAgent._generate_report')
    def test_run_success(self, mock_report, mock_retrieve, mock_search, mock_calc):
        # Setup mocks
        mock_calc.return_value = json.dumps({"total_tco2e": 100.0, "scope1_kg": 10})
        mock_search.return_value = json.dumps([{"title": "Offset 1"}])
        mock_retrieve.return_value = "Methodology text"
        mock_report.return_value = "Report generated: file.pdf"
        
        agent = CarbonFootprintAgent(model="mock")
        
        # Track emitted events
        emitted_events = []
        def emit_mock(event):
            emitted_events.append(event)
            
        test_data = {"company_name": "Test Corp"}
        
        result = agent.run(test_data, emit_thought=emit_mock)
        
        assert result["status"] == "complete"
        assert "emissions" in result
        assert result["emissions"]["total_tco2e"] == 100.0
        assert "report" in result
        
        # Check that events were emitted
        assert len(emitted_events) > 5
        assert any(e["type"] == "thought" for e in emitted_events)
        assert any(e["type"] == "action" for e in emitted_events)
        assert any(e["type"] == "observation" for e in emitted_events)
        assert any(e["type"] == "complete" for e in emitted_events)
