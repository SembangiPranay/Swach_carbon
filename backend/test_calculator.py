"""
Unit Tests for GHG Calculator Module

Tests verify that all calculations are accurate according to DEFRA/IPCC standards.
This is a critical module — accuracy is non-negotiable.

Run with: pytest test_calculator.py -v
"""

import pytest
from tools.calculator import (
    ActivityData,
    EmissionResult,
    EmissionFactors,
    calculate_scope1,
    calculate_scope2,
    calculate_scope3,
    calculate_emissions,
    get_industry_benchmark,
    calculate_benchmark_percentile,
)


# ============================================================================
# TESTS FOR SCOPE 1 (DIRECT EMISSIONS)
# ============================================================================

class TestScope1Calculations:
    """Tests for direct emissions from fuel burning"""

    def test_scope1_diesel_only(self):
        """Test: 500 litres of diesel = 1340 kg CO₂"""
        activity = ActivityData(diesel_litres=500)
        scope1_kg, breakdown = calculate_scope1(activity)

        assert scope1_kg == pytest.approx(1340.0)
        assert breakdown['diesel'] == pytest.approx(1340.0)

    def test_scope1_petrol_only(self):
        """Test: 300 litres petrol = 693 kg CO₂"""
        activity = ActivityData(petrol_litres=300)
        scope1_kg, breakdown = calculate_scope1(activity)

        expected = 300 * 2.31
        assert scope1_kg == pytest.approx(expected)

    def test_scope1_lpg_only(self):
        """Test: 100 kg LPG = 298 kg CO₂"""
        activity = ActivityData(lpg_kg=100)
        scope1_kg, breakdown = calculate_scope1(activity)

        expected = 100 * 2.98
        assert scope1_kg == pytest.approx(expected)

    def test_scope1_mixed_fuels(self):
        """Test: Multiple fuels add up correctly"""
        activity = ActivityData(
            diesel_litres=500,
            petrol_litres=300,
            lpg_kg=100,
            natural_gas_m3=50
        )
        scope1_kg, breakdown = calculate_scope1(activity)

        expected = (
            500 * 2.68 +
            300 * 2.31 +
            100 * 2.98 +
            50 * 2.04
        )
        assert scope1_kg == pytest.approx(expected)

    def test_scope1_zero_emissions(self):
        """Test: No fuel = 0 emissions"""
        activity = ActivityData()
        scope1_kg, breakdown = calculate_scope1(activity)

        assert scope1_kg == 0.0
        assert len(breakdown) == 0

    def test_scope1_breakdown_only_nonzero(self):
        """Test: Breakdown excludes zero-value items"""
        activity = ActivityData(diesel_litres=100, petrol_litres=0, lpg_kg=0)
        scope1_kg, breakdown = calculate_scope1(activity)

        assert 'diesel' in breakdown
        assert 'petrol' not in breakdown
        assert 'lpg' not in breakdown


# ============================================================================
# TESTS FOR SCOPE 2 (PURCHASED ELECTRICITY)
# ============================================================================

class TestScope2Calculations:
    """Tests for purchased electricity emissions (using India grid factor)"""

    def test_scope2_india_grid_factor(self):
        """Test: 10,000 kWh × 0.82 = 8,200 kg CO₂"""
        activity = ActivityData(electricity_kwh=10000)
        scope2_kg, breakdown = calculate_scope2(activity)

        expected = 10000 * 0.82
        assert scope2_kg == pytest.approx(8200.0)
        assert breakdown['electricity'] == pytest.approx(8200.0)

    def test_scope2_zero_electricity(self):
        """Test: 0 kWh = 0 emissions"""
        activity = ActivityData(electricity_kwh=0)
        scope2_kg, breakdown = calculate_scope2(activity)

        assert scope2_kg == 0.0

    def test_scope2_small_consumption(self):
        """Test: 1 kWh = 0.82 kg CO₂"""
        activity = ActivityData(electricity_kwh=1)
        scope2_kg, breakdown = calculate_scope2(activity)

        assert scope2_kg == pytest.approx(0.82)

    def test_scope2_large_consumption(self):
        """Test: Large industrial consumption"""
        activity = ActivityData(electricity_kwh=500000)  # 500 MWh
        scope2_kg, breakdown = calculate_scope2(activity)

        expected = 500000 * 0.82
        assert scope2_kg == pytest.approx(expected)


# ============================================================================
# TESTS FOR SCOPE 3 (INDIRECT/VALUE CHAIN)
# ============================================================================

class TestScope3Calculations:
    """Tests for indirect emissions (travel, commute, waste, supply chain)"""

    def test_scope3_domestic_flights(self):
        """Test: 2000 km domestic flight"""
        activity = ActivityData(flights_domestic_km=2000)
        scope3_kg, breakdown = calculate_scope3(activity)

        expected = 2000 * 0.240
        assert scope3_kg == pytest.approx(expected)
        assert 'flights' in breakdown

    def test_scope3_international_flights(self):
        """Test: 5000 km international flight (long-haul)"""
        activity = ActivityData(flights_international_km=5000)
        scope3_kg, breakdown = calculate_scope3(activity)

        expected = 5000 * 0.195
        assert scope3_kg == pytest.approx(expected)

    def test_scope3_employee_commute_car(self):
        """Test: 10,000 km employee car commuting"""
        activity = ActivityData(employee_commute_car_km=10000)
        scope3_kg, breakdown = calculate_scope3(activity)

        expected = 10000 * 0.21
        assert scope3_kg == pytest.approx(expected)

    def test_scope3_employee_commute_bus(self):
        """Test: 5000 km bus commuting (lower emissions)"""
        activity = ActivityData(employee_commute_bus_km=5000)
        scope3_kg, breakdown = calculate_scope3(activity)

        expected = 5000 * 0.089
        assert scope3_kg == pytest.approx(expected)

    def test_scope3_waste_landfill(self):
        """Test: 500 kg waste to landfill"""
        activity = ActivityData(waste_landfill_kg=500)
        scope3_kg, breakdown = calculate_scope3(activity)

        expected = 500 * 0.58
        assert scope3_kg == pytest.approx(expected)

    def test_scope3_waste_recycled(self):
        """Test: Recycled waste has lower emissions"""
        activity = ActivityData(waste_recycled_kg=500)
        scope3_kg, breakdown = calculate_scope3(activity)

        expected = 500 * 0.05
        assert scope3_kg == pytest.approx(expected)

    def test_scope3_supply_chain_spend(self):
        """Test: Supply chain spend-based calculation"""
        activity = ActivityData(supply_chain_spend_inr=100000)  # ₹100k spend
        scope3_kg, breakdown = calculate_scope3(activity)

        expected = 100000 * 0.00075
        assert scope3_kg == pytest.approx(expected)

    def test_scope3_combined_activities(self):
        """Test: Multiple Scope 3 activities sum correctly"""
        activity = ActivityData(
            flights_domestic_km=2000,
            employee_commute_car_km=10000,
            waste_landfill_kg=500,
        )
        scope3_kg, breakdown = calculate_scope3(activity)

        expected = (
            2000 * 0.240 +
            10000 * 0.21 +
            500 * 0.58
        )
        assert scope3_kg == pytest.approx(expected)
        assert len(breakdown) == 3

    def test_scope3_zero_emissions(self):
        """Test: No activities = 0 emissions"""
        activity = ActivityData()
        scope3_kg, breakdown = calculate_scope3(activity)

        assert scope3_kg == 0.0
        assert len(breakdown) == 0


# ============================================================================
# TESTS FOR COMPLETE CALCULATION
# ============================================================================

class TestCompleteCalculation:
    """Tests for the main calculate_emissions function"""

    def test_calculate_emissions_basic(self):
        """Test: Complete calculation with all three scopes"""
        activity = ActivityData(
            diesel_litres=500,          # Scope 1: 1340 kg
            electricity_kwh=10000,      # Scope 2: 8200 kg
            flights_domestic_km=2000,   # Scope 3: 480 kg
            waste_landfill_kg=500       # Scope 3: 290 kg
        )

        result = calculate_emissions(activity)

        # Expected totals
        expected_scope1 = 1340.0
        expected_scope2 = 8200.0
        expected_scope3 = 480 + 290  # 770

        assert result.scope1_kg == pytest.approx(expected_scope1)
        assert result.scope2_kg == pytest.approx(expected_scope2)
        assert result.scope3_kg == pytest.approx(expected_scope3)

        # Total should be in tonnes
        expected_total_kg = expected_scope1 + expected_scope2 + expected_scope3
        expected_total_tco2e = expected_total_kg / 1000
        assert result.total_tco2e == pytest.approx(expected_total_tco2e)

    def test_calculate_emissions_percentages(self):
        """Test: Percentage calculations are correct"""
        activity = ActivityData(
            diesel_litres=500,      # 1340 kg
            electricity_kwh=10000,  # 8200 kg
        )

        result = calculate_emissions(activity)

        total = 1340 + 8200  # 9540 kg
        expected_scope1_pct = (1340 / total) * 100  # ~14%
        expected_scope2_pct = (8200 / total) * 100  # ~86%

        assert result.scope1_percent == pytest.approx(expected_scope1_pct, rel=0.1)
        assert result.scope2_percent == pytest.approx(expected_scope2_pct, rel=0.1)

    def test_calculate_emissions_zero_case(self):
        """Test: Empty data returns zero"""
        activity = ActivityData()
        result = calculate_emissions(activity)

        assert result.scope1_kg == 0.0
        assert result.scope2_kg == 0.0
        assert result.scope3_kg == 0.0
        assert result.total_tco2e == 0.0

    def test_calculate_emissions_scope2_dominant(self):
        """Test: Case where Scope 2 dominates (typical IT company)"""
        activity = ActivityData(
            electricity_kwh=50000,  # 41,000 kg = 41 tCO₂e
            diesel_litres=100,      # 268 kg
        )

        result = calculate_emissions(activity)

        # Scope 2 should be ~99% of total
        assert result.scope2_percent > 95.0

    def test_calculate_emissions_scope1_dominant(self):
        """Test: Case where Scope 1 dominates (manufacturing)"""
        activity = ActivityData(
            diesel_litres=2000,      # 5360 kg
            natural_gas_m3=1000,     # 2040 kg
            electricity_kwh=5000,    # 4100 kg
        )

        result = calculate_emissions(activity)

        # Scope 1 should dominate (7400 > 4100)
        assert result.scope1_kg > result.scope2_kg

    def test_calculate_emissions_large_company(self):
        """Test: Large company with all emission sources"""
        activity = ActivityData(
            # Scope 1
            diesel_litres=1000,
            natural_gas_m3=500,
            # Scope 2
            electricity_kwh=100000,
            # Scope 3
            flights_domestic_km=50000,
            flights_international_km=30000,
            employee_commute_car_km=100000,
            waste_landfill_kg=5000,
            supply_chain_spend_inr=10000000,  # ₹1 crore
        )

        result = calculate_emissions(activity)

        # Should have all three scopes
        assert result.scope1_kg > 0
        assert result.scope2_kg > 0
        assert result.scope3_kg > 0
        assert result.total_tco2e > 0

        # Total should be reasonable (not more than expected)
        # ~3,700 + 82,000 + 24,500 = ~110 tCO₂e
        assert result.total_tco2e > 50  # At least 50 tCO₂e
        assert result.total_tco2e < 500  # But not crazy high

    def test_calculate_emissions_returns_result_object(self):
        """Test: Return type is EmissionResult"""
        activity = ActivityData(electricity_kwh=1000)
        result = calculate_emissions(activity)

        assert isinstance(result, EmissionResult)
        assert hasattr(result, 'scope1_kg')
        assert hasattr(result, 'scope2_kg')
        assert hasattr(result, 'scope3_kg')
        assert hasattr(result, 'total_tco2e')

    def test_calculate_emissions_breakdown_not_empty(self):
        """Test: Breakdown contains activity data"""
        activity = ActivityData(
            diesel_litres=100,
            electricity_kwh=5000,
            flights_domestic_km=1000,
        )

        result = calculate_emissions(activity)

        assert 'diesel' in result.breakdown_scope1
        assert 'electricity' in result.breakdown_scope2
        assert 'flights' in result.breakdown_scope3


# ============================================================================
# TESTS FOR DATA CONVERSION (Serialization)
# ============================================================================

class TestDataConversion:
    """Tests for converting data to/from dictionaries"""

    def test_activity_data_to_dict(self):
        """Test: ActivityData converts to dictionary"""
        activity = ActivityData(
            diesel_litres=100,
            electricity_kwh=5000,
            company_name="Test Corp"
        )

        data_dict = activity.to_dict()

        assert isinstance(data_dict, dict)
        assert data_dict['diesel_litres'] == 100
        assert data_dict['electricity_kwh'] == 5000

    def test_emission_result_to_dict(self):
        """Test: EmissionResult converts to JSON-serializable dict"""
        activity = ActivityData(
            diesel_litres=100,
            electricity_kwh=5000,
        )

        result = calculate_emissions(activity)
        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert 'scope1_kg' in result_dict
        assert 'scope2_kg' in result_dict
        assert 'total_tco2e' in result_dict
        assert 'breakdown' in result_dict

        # Values should be rounded
        assert isinstance(result_dict['scope1_kg'], float)


# ============================================================================
# TESTS FOR BENCHMARKING
# ============================================================================

class TestBenchmarking:
    """Tests for industry benchmarking functionality"""

    def test_get_industry_benchmark_it(self):
        """Test: IT industry benchmark exists"""
        benchmark = get_industry_benchmark('IT')
        assert benchmark is not None
        assert benchmark > 0

    def test_get_industry_benchmark_manufacturing(self):
        """Test: Manufacturing industry benchmark"""
        benchmark = get_industry_benchmark('Manufacturing')
        assert benchmark is not None
        assert benchmark > 100  # Manufacturing > IT

    def test_get_industry_benchmark_unknown(self):
        """Test: Unknown industry returns None"""
        benchmark = get_industry_benchmark('Unknown Industry')
        assert benchmark is None

    def test_calculate_benchmark_percentile_average(self):
        """Test: Company at industry average = 100%"""
        it_avg = get_industry_benchmark('IT')
        percentile = calculate_benchmark_percentile(it_avg, 'IT')

        assert percentile is not None
        assert percentile == pytest.approx(100.0)

    def test_calculate_benchmark_percentile_below_average(self):
        """Test: Company below average gets percentile < 100"""
        percentile = calculate_benchmark_percentile(50.0, 'IT')

        assert percentile is not None
        assert percentile < 100.0

    def test_calculate_benchmark_percentile_above_average(self):
        """Test: Company above average gets percentile > 100 (capped at 100)"""
        percentile = calculate_benchmark_percentile(500.0, 'Manufacturing')

        assert percentile is not None
        # Capped at 100 in actual code
        assert percentile <= 100.0


# ============================================================================
# REAL-WORLD SCENARIO TESTS
# ============================================================================

class TestRealWorldScenarios:
    """Tests based on realistic company profiles"""

    def test_scenario_small_it_startup(self):
        """Scenario: Small IT startup (50 employees, 1 office)"""
        activity = ActivityData(
            company_name="TechStartup Inc",
            industry="IT",
            # Mostly electricity (office/servers)
            electricity_kwh=50000,
            # Some diesel for backup generator
            diesel_litres=100,
            # Employee commuting and occasional flights
            employee_commute_car_km=50000,
            flights_domestic_km=5000,
            flights_international_km=10000,
            # Office waste
            waste_landfill_kg=500,
        )

        result = calculate_emissions(activity)

        # Should have reasonable emissions for small startup
        assert 30 < result.total_tco2e < 100

    def test_scenario_manufacturing_company(self):
        """Scenario: Manufacturing plant in India"""
        activity = ActivityData(
            company_name="MFG Corp",
            industry="Manufacturing",
            # Heavy fuel use
            diesel_litres=5000,
            natural_gas_m3=2000,
            # High electricity
            electricity_kwh=200000,
            # Business travel
            flights_domestic_km=20000,
            flights_international_km=30000,
            employee_commute_car_km=200000,
            # Waste from manufacturing
            waste_landfill_kg=10000,
            # Supply chain emissions
            supply_chain_spend_inr=50000000,  # ₹5 crore
        )

        result = calculate_emissions(activity)

        # Manufacturing should have high emissions (total 277 tCO₂e calculated)
        assert result.total_tco2e > 200

    def test_scenario_hospitality_chain(self):
        """Scenario: Hotel/hospitality business"""
        activity = ActivityData(
            company_name="Hotel Chain",
            industry="Hospitality",
            # Fuel for heating/hot water
            lpg_kg=1000,
            # High electricity (AC, lighting, cooking)
            electricity_kwh=100000,
            # Guest and employee travel
            flights_domestic_km=30000,
            employee_commute_car_km=100000,
            # Waste from guests
            waste_landfill_kg=5000,
        )

        result = calculate_emissions(activity)

        assert result.total_tco2e > 100
        # Scope 2 (electricity) should be significant
        assert result.scope2_percent > 40


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and boundary conditions"""

    def test_very_large_values(self):
        """Test: Handles very large emission sources"""
        activity = ActivityData(
            electricity_kwh=10000000,  # 10 million kWh
            diesel_litres=100000,      # 100,000 liters
        )

        result = calculate_emissions(activity)

        # Should still calculate correctly without overflow
        assert result.total_tco2e > 0
        assert result.total_tco2e != float('inf')
        assert result.scope1_kg != float('inf')
        assert result.scope2_kg != float('inf')

    def test_very_small_values(self):
        """Test: Handles very small values"""
        activity = ActivityData(
            electricity_kwh=0.001,
            diesel_litres=0.001,
        )

        result = calculate_emissions(activity)

        # Should still calculate correctly
        assert result.total_tco2e >= 0

    def test_negative_values_not_possible(self):
        """Test: Negative values (shouldn't happen, but test anyway)"""
        # ActivityData uses float, so negative is technically possible
        # In production, validation should prevent this
        activity = ActivityData(electricity_kwh=-100)

        result = calculate_emissions(activity)

        # Result will be negative, which is wrong
        # This test documents the behavior; validation should be in the API layer
        assert result.scope2_kg < 0

    def test_precision_with_rounding(self):
        """Test: Rounding doesn't lose significant information"""
        activity = ActivityData(electricity_kwh=12345)

        result = calculate_emissions(activity)
        result_dict = result.to_dict()

        # Rounded to 2 decimal places
        assert result_dict['scope2_kg'] == pytest.approx(10122.9, rel=0.01)


# ============================================================================
# RUN TESTS
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
