# Testing Reference Guide

## Running Tests

### Run all tests with verbose output
```bash
cd backend
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pytest test_calculator.py -v
```

### Run specific test class
```bash
pytest test_calculator.py::TestScope1Calculations -v
pytest test_calculator.py::TestScope2Calculations -v
pytest test_calculator.py::TestScope3Calculations -v
pytest test_calculator.py::TestCompleteCalculation -v
```

### Run specific test
```bash
pytest test_calculator.py::TestScope1Calculations::test_scope1_diesel_only -v
```

### Show test output details
```bash
pytest test_calculator.py -vv  # Extra verbose
pytest test_calculator.py -s   # Show print statements
```

### Run with coverage (if installed)
```bash
pip install pytest-cov
pytest test_calculator.py --cov=tools --cov-report=html
```

---

## Test Categories (42 Total)

### TestScope1Calculations (6 tests)
Tests for Scope 1 - Direct emissions from fuel burning
- `test_scope1_diesel_only` - Diesel calculation
- `test_scope1_petrol_only` - Petrol calculation
- `test_scope1_lpg_only` - LPG calculation
- `test_scope1_mixed_fuels` - Multiple fuels together
- `test_scope1_zero_emissions` - Zero emissions edge case
- `test_scope1_breakdown_only_nonzero` - Only non-zero items in breakdown

### TestScope2Calculations (4 tests)
Tests for Scope 2 - Purchased electricity emissions
- `test_scope2_india_grid_factor` - India grid (0.82 kg CO₂/kWh)
- `test_scope2_zero_electricity` - Zero electricity edge case
- `test_scope2_small_consumption` - 1 kWh consumption
- `test_scope2_large_consumption` - 500,000 kWh consumption

### TestScope3Calculations (9 tests)
Tests for Scope 3 - Indirect value chain emissions
- `test_scope3_domestic_flights` - Domestic flight calculation
- `test_scope3_international_flights` - International flights
- `test_scope3_employee_commute_car` - Car commuting
- `test_scope3_employee_commute_bus` - Bus commuting
- `test_scope3_waste_landfill` - Waste to landfill
- `test_scope3_waste_recycled` - Recycled waste (lower emissions)
- `test_scope3_supply_chain_spend` - Supply chain spend-based
- `test_scope3_combined_activities` - Multiple activities
- `test_scope3_zero_emissions` - Zero emissions edge case

### TestCompleteCalculation (8 tests)
Tests for the main calculate_emissions function
- `test_calculate_emissions_basic` - Full calculation
- `test_calculate_emissions_percentages` - Percentage calculations
- `test_calculate_emissions_zero_case` - Empty input
- `test_calculate_emissions_scope2_dominant` - Scope 2 heavy (typical IT)
- `test_calculate_emissions_scope1_dominant` - Scope 1 heavy (manufacturing)
- `test_calculate_emissions_large_company` - Large company all sources
- `test_calculate_emissions_returns_result_object` - Type checking
- `test_calculate_emissions_breakdown_not_empty` - Breakdown structure

### TestDataConversion (2 tests)
Tests for data serialization
- `test_activity_data_to_dict` - ActivityData to dictionary
- `test_emission_result_to_dict` - EmissionResult to dictionary

### TestBenchmarking (6 tests)
Tests for industry benchmarking
- `test_get_industry_benchmark_it` - IT industry benchmark
- `test_get_industry_benchmark_manufacturing` - Manufacturing benchmark
- `test_get_industry_benchmark_unknown` - Unknown industry
- `test_calculate_benchmark_percentile_average` - Average percentile
- `test_calculate_benchmark_percentile_below_average` - Below average
- `test_calculate_benchmark_percentile_above_average` - Above average

### TestRealWorldScenarios (3 tests)
Tests based on realistic company profiles
- `test_scenario_small_it_startup` - Small IT startup (55 tCO₂e)
- `test_scenario_manufacturing_company` - Manufacturing plant (277 tCO₂e)
- `test_scenario_hospitality_chain` - Hotel chain (116 tCO₂e)

### TestEdgeCases (4 tests)
Tests for boundary conditions and edge cases
- `test_very_large_values` - Very large numbers
- `test_very_small_values` - Very small numbers
- `test_negative_values_not_possible` - Negative values (shouldn't happen)
- `test_precision_with_rounding` - Rounding accuracy

---

## Demo Script

Run the demo to see the calculator in action:

```bash
cd backend
python demo_calculator.py
```

### Demo Output Includes:
1. **Small IT Startup** - 55.21 tCO₂e (74% from electricity)
2. **Manufacturing Company** - 277.43 tCO₂e (59% from electricity)
3. **Hospitality Chain** - 116.08 tCO₂e (71% from electricity)
4. **Company Comparison** - Side-by-side three company types

Each demo shows:
- Total emissions in tCO₂e
- Breakdown by scope (1, 2, 3)
- Breakdown by source (diesel, electricity, flights, etc.)
- Offset costs at ₹400/tonne

---

## Quick Calculator Usage

```python
from tools.calculator import ActivityData, calculate_emissions

# Create activity data
data = ActivityData(
    company_name="TechCorp",
    industry="IT",
    electricity_kwh=50000,
    diesel_litres=100,
    flights_domestic_km=5000,
    waste_landfill_kg=500
)

# Calculate
result = calculate_emissions(data)

# Access results
print(result.total_tco2e)        # 55.21 tCO₂e
print(result.scope1_kg)          # 268 kg
print(result.scope2_kg)          # 41000 kg
print(result.scope3_kg)          # 13940 kg

# Breakdown
print(result.breakdown_scope1)   # {'diesel': 268}
print(result.breakdown_scope2)   # {'electricity': 41000}
print(result.breakdown_scope3)   # {'flights': 3150, 'employee_commute': 10500, 'waste': 290}

# Percentages
print(result.scope1_percent)     # 0.5%
print(result.scope2_percent)     # 74.3%
print(result.scope3_percent)     # 25.2%

# JSON for API
json_data = result.to_dict()
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'tools'"
```bash
# Make sure you're in the backend directory
cd backend
python -m pytest test_calculator.py -v
```

### "UnicodeEncodeError" with emoji characters
- This is a Windows console encoding issue
- The demo script has been fixed - use latest version
- Or set environment: `set PYTHONIOENCODING=utf-8`

### Tests fail with import errors
```bash
# Reinstall requirements
pip install -r requirements.txt
pytest test_calculator.py -v
```

### Virtual environment not working
```bash
# Recreate venv
rm -r venv          # Or: rmdir /s venv (Windows)
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

---

## Continuous Integration (GitHub)

When you add to GitHub, create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest test_calculator.py -v
```

This will auto-run tests on every push!

---

## Verification Checklist

Before moving to Day 3, verify:

- [ ] 42 tests passing
- [ ] Demo script runs without errors
- [ ] Can import: `from tools.calculator import calculate_emissions`
- [ ] Calculator handles zero inputs gracefully
- [ ] Large values (1M kWh) don't cause overflow
- [ ] Results are in reasonable ranges

Quick verification command:
```bash
cd backend
python -c "from tools.calculator import *; print('✓ All imports OK'); from test_calculator import *; print('✓ Tests importable')"
```

---

## Expected Test Output

```
============================= test session starts =============================
platform win32 -- Python 3.14.3, pytest-9.0.3, pluggy-1.6.0
collected 42 items

test_calculator.py::TestScope1Calculations::test_scope1_diesel_only PASSED [  2%]
test_calculator.py::TestScope1Calculations::test_scope1_petrol_only PASSED [  4%]
...
test_calculator.py::TestEdgeCases::test_precision_with_rounding PASSED [100%]

============================= 42 passed in 0.13s ==============================
```

**Green means all good!** ✅

