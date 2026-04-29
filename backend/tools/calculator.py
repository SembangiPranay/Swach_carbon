"""
GHG Protocol Calculator Module

Calculates Scope 1, 2, and 3 emissions using official DEFRA and IPCC emission factors.
This module is deterministic and audit-ready — no AI approximations, pure math.

All factors are based on:
- DEFRA (UK Department for Business, Energy and Industrial Strategy) 2024
- IPCC Guidelines 2024
- India Ministry of Power Grid Factor 2024
"""

from dataclasses import dataclass
from typing import Dict, Optional
from enum import Enum


# ============================================================================
# EMISSION FACTORS (Official Standards)
# ============================================================================

class EmissionFactors:
    """
    Official emission factors from DEFRA and IPCC.
    These should NOT be changed without regulatory update.
    Unit: kg CO₂ per unit of activity
    """

    # SCOPE 1: DIRECT EMISSIONS
    DIESEL_LITRES = 2.68  # kg CO₂ per litre (DEFRA 2024)
    PETROL_LITRES = 2.31  # kg CO₂ per litre
    LPG_KG = 2.98  # kg CO₂ per kg
    NATURAL_GAS_M3 = 2.04  # kg CO₂ per cubic meter
    COAL_TONNES = 2420.0  # kg CO₂ per tonne

    # SCOPE 2: PURCHASED ELECTRICITY
    # India's grid is coal-heavy, so emission factor is higher than developed nations
    INDIA_GRID_KWH = 0.82  # kg CO₂ per kWh (Ministry of Power 2024)
    WORLD_AVG_GRID_KWH = 0.475  # kg CO₂ per kWh (for reference)

    # SCOPE 3: INDIRECT EMISSIONS
    # Business Travel
    FLIGHTS_SHORT_HAUL_KM = 0.255  # kg CO₂ per km (distance <900km)
    FLIGHTS_LONG_HAUL_KM = 0.195  # kg CO₂ per km (distance >900km)
    FLIGHTS_DOMESTIC_KM = 0.240  # kg CO₂ per km (India domestic)

    # Employee Commuting
    CAR_AVERAGE_KM = 0.21  # kg CO₂ per km (average car)
    BUS_KM = 0.089  # kg CO₂ per km (public transport)
    TRAIN_KM = 0.041  # kg CO₂ per km (rail)
    MOTORCYCLE_KM = 0.12  # kg CO₂ per km

    # Waste Management
    WASTE_LANDFILL_KG = 0.58  # kg CO₂ per kg (includes methane decomposition)
    WASTE_INCINERATION_KG = 0.35  # kg CO₂ per kg
    WASTE_RECYCLED_KG = 0.05  # kg CO₂ per kg (minimal)

    # Water
    WATER_M3 = 0.344  # kg CO₂ per cubic meter

    # Supply Chain (Spend-based method)
    SUPPLY_CHAIN_PER_INR = 0.00075  # kg CO₂ per ₹ spent (Indian average)


# ============================================================================
# DATA CLASSES FOR TYPE SAFETY
# ============================================================================

@dataclass
class ActivityData:
    """Input data from company operations"""

    # SCOPE 1: Direct emissions (on-site fuel burning)
    diesel_litres: float = 0.0
    petrol_litres: float = 0.0
    lpg_kg: float = 0.0
    natural_gas_m3: float = 0.0
    coal_tonnes: float = 0.0

    # SCOPE 2: Purchased electricity
    electricity_kwh: float = 0.0

    # SCOPE 3: Indirect emissions
    # Travel
    flights_domestic_km: float = 0.0
    flights_international_km: float = 0.0
    employee_commute_car_km: float = 0.0
    employee_commute_bus_km: float = 0.0
    employee_commute_train_km: float = 0.0

    # Waste & Water
    waste_landfill_kg: float = 0.0
    waste_incineration_kg: float = 0.0
    waste_recycled_kg: float = 0.0
    water_m3: float = 0.0

    # Supply chain (optional - for more sophisticated analysis)
    supply_chain_spend_inr: float = 0.0

    # Metadata
    company_name: str = "Company"
    industry: str = "Unknown"
    employee_count: int = 1

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            'diesel_litres': self.diesel_litres,
            'petrol_litres': self.petrol_litres,
            'lpg_kg': self.lpg_kg,
            'natural_gas_m3': self.natural_gas_m3,
            'coal_tonnes': self.coal_tonnes,
            'electricity_kwh': self.electricity_kwh,
            'flights_domestic_km': self.flights_domestic_km,
            'flights_international_km': self.flights_international_km,
            'employee_commute_car_km': self.employee_commute_car_km,
            'employee_commute_bus_km': self.employee_commute_bus_km,
            'employee_commute_train_km': self.employee_commute_train_km,
            'waste_landfill_kg': self.waste_landfill_kg,
            'waste_incineration_kg': self.waste_incineration_kg,
            'waste_recycled_kg': self.waste_recycled_kg,
            'water_m3': self.water_m3,
            'supply_chain_spend_inr': self.supply_chain_spend_inr,
            'industry': self.industry,
            'employee_count': self.employee_count,
        }


@dataclass
class EmissionResult:
    """Output: Calculated emissions"""

    # Individual scope totals (in kg CO₂)
    scope1_kg: float
    scope2_kg: float
    scope3_kg: float

    # Total emissions (in tonnes CO₂ equivalent)
    total_tco2e: float

    # Breakdown by source (for visualization)
    breakdown_scope1: Dict[str, float]  # {'diesel': X, 'lpg': Y, ...}
    breakdown_scope2: Dict[str, float]  # {'electricity': X}
    breakdown_scope3: Dict[str, float]  # {'flights': X, 'commute': Y, 'waste': Z}

    # Percentages for charts
    scope1_percent: float
    scope2_percent: float
    scope3_percent: float

    # Industry benchmarking (to be populated later)
    industry_average_tco2e: Optional[float] = None
    benchmark_percentile: Optional[float] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization/JSON"""
        return {
            'scope1_kg': round(self.scope1_kg, 2),
            'scope2_kg': round(self.scope2_kg, 2),
            'scope3_kg': round(self.scope3_kg, 2),
            'total_tco2e': round(self.total_tco2e, 2),
            'scope1_percent': round(self.scope1_percent, 1),
            'scope2_percent': round(self.scope2_percent, 1),
            'scope3_percent': round(self.scope3_percent, 1),
            'breakdown': {
                'scope1': self.breakdown_scope1,
                'scope2': self.breakdown_scope2,
                'scope3': self.breakdown_scope3,
            },
            'benchmarking': {
                'industry_average_tco2e': self.industry_average_tco2e,
                'benchmark_percentile': self.benchmark_percentile,
            }
        }


# ============================================================================
# CALCULATION FUNCTIONS (Pure Math)
# ============================================================================

def calculate_scope1(activity_data: ActivityData) -> tuple[float, Dict[str, float]]:
    """
    Calculate Scope 1 emissions (Direct emissions from fuel burning on-site)

    Returns:
        tuple: (total_kg_co2, breakdown_dict)
    """
    breakdown = {
        'diesel': activity_data.diesel_litres * EmissionFactors.DIESEL_LITRES,
        'petrol': activity_data.petrol_litres * EmissionFactors.PETROL_LITRES,
        'lpg': activity_data.lpg_kg * EmissionFactors.LPG_KG,
        'natural_gas': activity_data.natural_gas_m3 * EmissionFactors.NATURAL_GAS_M3,
        'coal': activity_data.coal_tonnes * EmissionFactors.COAL_TONNES,
    }

    total_kg = sum(breakdown.values())
    return total_kg, {k: v for k, v in breakdown.items() if v > 0}  # Only non-zero items


def calculate_scope2(activity_data: ActivityData) -> tuple[float, Dict[str, float]]:
    """
    Calculate Scope 2 emissions (Purchased electricity)

    Returns:
        tuple: (total_kg_co2, breakdown_dict)
    """
    # Using India grid emission factor (0.82 kg CO₂/kWh - coal heavy)
    electricity_emissions = activity_data.electricity_kwh * EmissionFactors.INDIA_GRID_KWH

    breakdown = {
        'electricity': electricity_emissions,
    }

    return electricity_emissions, breakdown


def calculate_scope3(activity_data: ActivityData) -> tuple[float, Dict[str, float]]:
    """
    Calculate Scope 3 emissions (Indirect value chain emissions)

    Includes:
    - Business travel (flights, taxis)
    - Employee commuting
    - Waste management
    - Supply chain (spend-based)

    Returns:
        tuple: (total_kg_co2, breakdown_dict)
    """
    breakdown = {}

    # Business Travel
    flights_emissions = (
        activity_data.flights_domestic_km * EmissionFactors.FLIGHTS_DOMESTIC_KM +
        activity_data.flights_international_km * EmissionFactors.FLIGHTS_LONG_HAUL_KM
    )
    if flights_emissions > 0:
        breakdown['flights'] = flights_emissions

    # Employee Commuting
    commute_emissions = (
        activity_data.employee_commute_car_km * EmissionFactors.CAR_AVERAGE_KM +
        activity_data.employee_commute_bus_km * EmissionFactors.BUS_KM +
        activity_data.employee_commute_train_km * EmissionFactors.TRAIN_KM
    )
    if commute_emissions > 0:
        breakdown['employee_commute'] = commute_emissions

    # Waste Management & Water
    waste_emissions = (
        activity_data.waste_landfill_kg * EmissionFactors.WASTE_LANDFILL_KG +
        activity_data.waste_incineration_kg * EmissionFactors.WASTE_INCINERATION_KG +
        activity_data.waste_recycled_kg * EmissionFactors.WASTE_RECYCLED_KG
    )
    if waste_emissions > 0:
        breakdown['waste'] = waste_emissions

    water_emissions = activity_data.water_m3 * EmissionFactors.WATER_M3
    if water_emissions > 0:
        breakdown['water'] = water_emissions

    # Supply Chain (Spend-based method)
    supply_chain_emissions = activity_data.supply_chain_spend_inr * EmissionFactors.SUPPLY_CHAIN_PER_INR
    if supply_chain_emissions > 0:
        breakdown['supply_chain'] = supply_chain_emissions

    total_kg = sum(breakdown.values())
    return total_kg, breakdown


# ============================================================================
# MAIN CALCULATOR FUNCTION
# ============================================================================

def calculate_emissions(activity_data: ActivityData) -> EmissionResult:
    """
    Calculate Scope 1, 2, 3 emissions and return comprehensive result.

    This is the core calculation engine. It:
    1. Calculates each scope accurately
    2. Totals all emissions
    3. Calculates percentages
    4. Returns audit-ready data

    Args:
        activity_data: Company operational data

    Returns:
        EmissionResult: Comprehensive emission calculation
    """

    # Calculate each scope
    scope1_kg, breakdown_scope1 = calculate_scope1(activity_data)
    scope2_kg, breakdown_scope2 = calculate_scope2(activity_data)
    scope3_kg, breakdown_scope3 = calculate_scope3(activity_data)

    # Total emissions
    total_kg_co2 = scope1_kg + scope2_kg + scope3_kg
    total_tco2e = total_kg_co2 / 1000  # Convert kg to tonnes

    # Calculate percentages (handle division by zero)
    if total_kg_co2 > 0:
        scope1_percent = (scope1_kg / total_kg_co2) * 100
        scope2_percent = (scope2_kg / total_kg_co2) * 100
        scope3_percent = (scope3_kg / total_kg_co2) * 100
    else:
        scope1_percent = scope2_percent = scope3_percent = 0.0

    result = EmissionResult(
        scope1_kg=scope1_kg,
        scope2_kg=scope2_kg,
        scope3_kg=scope3_kg,
        total_tco2e=total_tco2e,
        breakdown_scope1=breakdown_scope1,
        breakdown_scope2=breakdown_scope2,
        breakdown_scope3=breakdown_scope3,
        scope1_percent=scope1_percent,
        scope2_percent=scope2_percent,
        scope3_percent=scope3_percent,
    )

    return result


# ============================================================================
# HELPER FUNCTIONS FOR BENCHMARKING (Future Use)
# ============================================================================

def get_industry_benchmark(industry: str) -> Optional[float]:
    """
    Get average emissions for an industry (tCO₂e/year).

    This is a placeholder — would be populated from Indian
    industry-specific databases or CSE reports.

    Args:
        industry: Industry name (e.g., "IT", "Manufacturing", "Retail")

    Returns:
        Average emissions for that industry, or None if unknown
    """
    # Industry benchmarks (these should come from CSE, CEMS, or industry reports)
    benchmarks = {
        'IT': 150.0,  # tCO₂e/year (typical IT company)
        'Manufacturing': 1200.0,
        'Retail': 250.0,
        'Hospitality': 400.0,
        'Logistics': 850.0,
        'Unknown': None,
    }

    return benchmarks.get(industry, None)


def calculate_benchmark_percentile(
    company_emissions: float,
    industry: str
) -> Optional[float]:
    """
    Calculate where a company sits in its industry.

    Args:
        company_emissions: Company's total tCO₂e
        industry: Industry category

    Returns:
        Percentile (0-100) where 100 = highest emissions
    """
    industry_avg = get_industry_benchmark(industry)

    if industry_avg is None:
        return None

    # Simple percentile: company emissions / industry average * 100
    percentile = min(100.0, (company_emissions / industry_avg) * 100)
    return percentile
