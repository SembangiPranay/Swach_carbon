import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from tools.vision_analyzer import UtilityBillAnalyzer, analyze_utility_bill

class TestVisionAnalyzer:
    
    @patch('tools.vision_analyzer.ChatGoogleGenerativeAI')
    @patch.dict('os.environ', {'GEMINI_API_KEY': 'fake_key'})
    def test_init_success(self, mock_gemini):
        analyzer = UtilityBillAnalyzer()
        assert analyzer.model_name == "gemini-1.5-pro"
        mock_gemini.assert_called_once()
        
    @patch('tools.vision_analyzer.ChatGoogleGenerativeAI')
    @patch.dict('os.environ', clear=True)
    def test_init_no_api_key(self, mock_gemini):
        analyzer = UtilityBillAnalyzer()
        assert analyzer.llm is None
        mock_gemini.assert_not_called()

    @patch('tools.vision_analyzer.os.path.exists')
    def test_analyze_bill_no_llm(self, mock_exists):
        analyzer = UtilityBillAnalyzer()
        analyzer.llm = None
        
        result = analyzer.analyze_bill("test.jpg")
        result_dict = json.loads(result)
        assert "error" in result_dict
        
    @patch('tools.vision_analyzer.os.path.exists')
    def test_analyze_bill_no_file(self, mock_exists):
        analyzer = UtilityBillAnalyzer()
        analyzer.llm = MagicMock()
        mock_exists.return_value = False
        
        result = analyzer.analyze_bill("test.jpg")
        result_dict = json.loads(result)
        assert "error" in result_dict
        
    @patch('tools.vision_analyzer.os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data=b"fake_image_data")
    def test_analyze_bill_success(self, mock_file, mock_exists):
        analyzer = UtilityBillAnalyzer()
        analyzer.llm = MagicMock()
        mock_exists.return_value = True
        
        # Mock LLM response
        mock_response = MagicMock()
        mock_response.content = '```json\n{"company_name": "Test Power", "electricity_kwh": 500}\n```'
        analyzer.llm.invoke.return_value = mock_response
        
        result = analyzer.analyze_bill("test.jpg", "electricity")
        result_dict = json.loads(result)
        
        assert result_dict["company_name"] == "Test Power"
        assert result_dict["electricity_kwh"] == 500
        
        # Verify LLM was called with the right parameters
        mock_invoke = analyzer.llm.invoke
        mock_invoke.assert_called_once()
        args = mock_invoke.call_args[0][0]
        assert len(args) == 1 # One message
        assert "electricity" in args[0].content[0]["text"]
        
    @patch('tools.vision_analyzer.UtilityBillAnalyzer.analyze_bill')
    def test_tool_wrapper(self, mock_analyze):
        mock_analyze.return_value = '{"success": true}'
        
        result = analyze_utility_bill("path.jpg", "water")
        
        assert result == '{"success": true}'
        mock_analyze.assert_called_once_with("path.jpg", "water")
