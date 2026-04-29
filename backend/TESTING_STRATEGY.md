# Backend Testing Strategy - Swach AI Carbon Agent

## Overview
Target: 70%+ test coverage focusing on critical business logic

## Test Structure

### Backend (/tests directory)
```
tests/
├── __init__.py
├── conftest.py                 # Pytest fixtures & configuration
├── unit/
│   ├── __init__.py
│   ├── test_models.py          # Pydantic models validation
│   ├── test_config.py          # Configuration & env setup
│   ├── test_calculations.py    # Carbon emission calculations (CRITICAL)
│   └── test_utils.py           # Utility functions
├── integration/
│   ├── __init__.py
│   ├── test_api_health.py      # Health endpoints
│   ├── test_api_calculate.py   # POST /calculate endpoint
│   ├── test_api_stream.py      # GET /stream endpoint
│   └── test_api_report.py      # GET /report endpoint
└── fixtures/
    ├── __init__.py
    └── sample_data.py          # Reusable test data
```

## Coverage Goals

| Module | Target | Priority |
|--------|--------|----------|
| models.py | 95% | Critical (validates all input) |
| config.py | 90% | High (env setup) |
| agent.py | 70% | High (complex logic) |
| main.py | 60% | Medium (routing) |
| middleware.py | 80% | High (security) |
| **TOTAL** | **70%** | **Portfolio** |

## Test Priority Order

### Priority 1: Business Logic (Most Important for Recruiters)
1. **test_calculations.py** - Emission calculations (GHG Protocol compliance)
2. **test_models.py** - Request validation
3. **test_api_calculate.py** - Main endpoint

### Priority 2: API Contract
1. **test_api_stream.py** - Real-time streaming
2. **test_api_report.py** - PDF generation
3. **test_api_health.py** - Health checks

### Priority 3: Infrastructure
1. **test_config.py** - Configuration
2. **test_middleware.py** - Rate limiting, CORS
3. **test_utils.py** - Helpers

## Key Testing Concepts You'll Learn

### 1. Unit Testing (Testing functions in isolation)
- Mock external dependencies (LLM, APIs)
- Test edge cases
- Test error handling
- **Why:** Ensures each function works correctly

### 2. Integration Testing (Testing components together)
- Test actual API endpoints
- Use test client
- Test database interactions
- **Why:** Ensures systems work together

### 3. Fixtures (Reusable test data)
- Sample company data
- Sample emissions data
- Test configurations
- **Why:** DRY principle for tests

### 4. Mocking (Simulating external services)
- Mock LLM responses
- Mock external APIs (Tavily, Gemini)
- Mock database
- **Why:** Tests don't depend on external services

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/unit/test_calculations.py

# Run tests matching pattern
pytest -k "test_calculate"

# Run with verbose output
pytest -v
```

## Recruitment Gold

These tests show recruiters:
- ✅ You understand testing best practices
- ✅ You can write comprehensive test suites
- ✅ You understand business logic (emission calculations)
- ✅ You know how to mock external dependencies
- ✅ You think about edge cases
- ✅ You prioritize critical functionality
