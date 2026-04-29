import pytest
import os
from unittest.mock import patch
from tools.pdf_gen import PDFReportGenerator, generate_pdf_report

class TestPDFGenerator:
    
    def test_init_pdf_generator(self):
        generator = PDFReportGenerator()
        assert "CustomTitle" in generator.styles
        assert "SectionTitle" in generator.styles
        
    def test_format_number(self):
        generator = PDFReportGenerator()
        assert generator._format_number(1234.567) == "1,234.57"
        assert generator._format_number(1000000) == "1,000,000.00"
        
    @patch('tools.pdf_gen.SimpleDocTemplate')
    def test_generate_report_basic(self, mock_doc):
        # We just mock the actual PDF building to avoid creating files in simple unit tests
        mock_instance = mock_doc.return_value
        
        generator = PDFReportGenerator()
        
        test_activity = {
            "electricity_kwh": 10000,
            "diesel_litres": 500
        }
        
        test_emission = {
            "total_tco2e": 50.5,
            "scope1_kg": 1000.0,
            "scope2_kg": 4000.0,
            "scope3_kg": 5000.0,
            "scope1_percent": 10.0,
            "scope2_percent": 40.0,
            "scope3_percent": 50.0,
            "breakdown": {
                "scope1": {"diesel": 1000.0},
                "scope2": {"electricity": 4000.0},
                "scope3": {}
            }
        }
        
        result = generator.generate_report(
            filename="test.pdf",
            company_name="Test Company",
            activity_data=test_activity,
            emission_result=test_emission
        )
        
        assert result == "test.pdf"
        mock_instance.build.assert_called_once()
        
        # Verify that elements were passed to build
        elements = mock_instance.build.call_args[0][0]
        assert len(elements) > 0

    @patch('tools.pdf_gen.PDFReportGenerator.generate_report')
    def test_generate_pdf_report_wrapper(self, mock_generate):
        mock_generate.return_value = "reports/report_Test_Co.pdf"
        
        result = generate_pdf_report(
            company_name="Test Co",
            activity_data={},
            emission_result={},
            output_dir="test_reports"
        )
        
        assert result == "reports/report_Test_Co.pdf"
        assert mock_generate.call_args[1]['company_name'] == "Test Co"
        assert mock_generate.call_args[1]['filename'] == "test_reports/report_Test_Co.pdf"
