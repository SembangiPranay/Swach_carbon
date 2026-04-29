"""
Pytest configuration and fixtures
Central place for test setup, mocks, and reusable test data
"""

import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
from datetime import datetime

# Set test environment
os.environ["DEBUG"] = "true"
os.environ["GROQ_API_KEY"] = "test-key-groq"
os.environ["TAVILY_API_KEY"] = "test-key-tavily"
os.environ["GEMINI_API_KEY"] = "test-key-gemini"


# ──── FastAPI Test Client ────────────────────────────────────────────────
@pytest.fixture
def client():
    """FastAPI test client"""
    from main import app
    return TestClient(app)


# ──── Sample Test Data ────────────────────────────────────────────────────
@pytest.fixture
def valid_activity_data():
    """Valid emission data for testing"""
    return {
        "company_name": "TestCorp India",
        "industry": "Technology",
        "employee_count": 500,

        # Scope 1 (Direct)
        "diesel_litres": 500,
        "petrol_litres": 200,
        "natural_gas_m3": 100,
        "lpg_kg": 50,
        "coal_tonnes": 0,

        # Scope 2 (Electricity)
        "electricity_kwh": 10000,

        # Scope 3 (Indirect)
        "flights_km": 2000,
        "commute_km": 5000,
        "waste_kg": 500,
        "water_m3": 1000,
    }


@pytest.fixture
def minimal_activity_data():
    """Minimal valid data (only required fields)"""
    return {
        "company_name": "MinimalCorp",
        "industry": "Manufacturing",
        "employee_count": 1,
    }


@pytest.fixture
def edge_case_data():
    """Edge case: very large numbers"""
    return {
        "company_name": "MegaCorp",
        "industry": "Energy",
        "employee_count": 100000,
        "electricity_kwh": 999999999,
        "diesel_litres": 999999,
    }


# ──── Mocks ──────────────────────────────────────────────────────────────
@pytest.fixture
def mock_llm():
    """Mock LLM responses"""
    mock = MagicMock()
    mock.invoke.return_value = "Test response"
    return mock


@pytest.fixture
def mock_groq():
    """Mock Groq LLM"""
    with patch("agent.ChatGroq") as mock:
        mock.return_value = MagicMock()
        yield mock


@pytest.fixture
def mock_gemini():
    """Mock Google Gemini"""
    with patch("agent.ChatGoogleGenerativeAI") as mock:
        mock.return_value = MagicMock()
        yield mock


@pytest.fixture
def mock_tavily():
    """Mock Tavily search API"""
    with patch("tools.tavily_client") as mock:
        mock.search.return_value = {
            "results": [
                {
                    "title": "Carbon Offset Project",
                    "url": "https://example.com",
                    "snippet": "Carbon offset description"
                }
            ]
        }
        yield mock


# ──── Configuration ──────────────────────────────────────────────────────
@pytest.fixture
def test_config():
    """Test configuration"""
    from config import Config
    return Config


# ──── Logger ─────────────────────────────────────────────────────────────
@pytest.fixture
def caplog_json(caplog):
    """Capture JSON logs"""
    return caplog


# ──── Markers ────────────────────────────────────────────────────────────
def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "critical: mark test as critical business logic"
    )
