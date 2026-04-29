"""
Quick demo of the GHG Calculator

This script shows how to use the calculator module to compute emissions.
Run with: python demo_calculator.py
"""

from tools.calculator import ActivityData, calculate_emissions


def print_result(result):
    """Pretty print emission results"""
    print("\n" + "="*60)
    print("EMISSION CALCULATION RESULTS")
    print("="*60)

    print(f"\nTOTAL EMISSIONS: {result.total_tco2e:.2f} tCO2e")
    print(f"   Scope 1 (Direct):      {result.scope1_kg:>10,.0f} kg ({result.scope1_percent:>5.1f}%)")
    print(f"   Scope 2 (Electricity): {result.scope2_kg:>10,.0f} kg ({result.scope2_percent:>5.1f}%)")
    print(f"   Scope 3 (Indirect):    {result.scope3_kg:>10,.0f} kg ({result.scope3_percent:>5.1f}%)")

    print("\nBREAKDOWN BY SOURCE:")

    if result.breakdown_scope1:
        print("   Scope 1:")
        for source, value in result.breakdown_scope1.items():
            print(f"      * {source.capitalize()}: {value:>10,.0f} kg")

    if result.breakdown_scope2:
        print("   Scope 2:")
        for source, value in result.breakdown_scope2.items():
            print(f"      * {source.capitalize()}: {value:>10,.0f} kg")

    if result.breakdown_scope3:
        print("   Scope 3:")
        for source, value in result.breakdown_scope3.items():
            print(f"      * {source.capitalize()}: {value:>10,.0f} kg")

    print("\nOFFSET COST (at Rs 400/tonne):")
    cost_100 = result.total_tco2e * 400
    cost_50 = cost_100 * 0.5
    cost_25 = cost_100 * 0.25

    print(f"   * 25% offset: Rs {cost_25:>12,.0f}")
    print(f"   * 50% offset: Rs {cost_50:>12,.0f}")
    print(f"   * 100% offset: Rs {cost_100:>12,.0f}")

    print("\n" + "="*60 + "\n")


def demo_small_startup():
    """Demo 1: Small IT startup"""
    print("\n[DEMO 1] Small IT Startup (50 employees)")
    print("-" * 60)

    activity = ActivityData(
        company_name="TechStartup Inc",
        industry="IT",
        electricity_kwh=50000,           # Office servers, AC
        diesel_litres=100,               # Backup generator
        employee_commute_car_km=50000,   # 50k km/year
        flights_domestic_km=5000,        # Domestic business travel
        flights_international_km=10000,  # International conferences
        waste_landfill_kg=500,           # Office waste
    )

    result = calculate_emissions(activity)
    print_result(result)


def demo_manufacturing():
    """Demo 2: Manufacturing company"""
    print("\n[DEMO 2] Manufacturing Company (500 employees)")
    print("-" * 60)

    activity = ActivityData(
        company_name="MFG Corp",
        industry="Manufacturing",
        diesel_litres=5000,              # Plant operations
        natural_gas_m3=2000,             # Furnaces, heating
        electricity_kwh=200000,          # Heavy machinery
        flights_domestic_km=20000,
        flights_international_km=30000,
        employee_commute_car_km=200000,
        waste_landfill_kg=10000,         # Manufacturing waste
        supply_chain_spend_inr=50000000, # Rs 5 crore supply chain
    )

    result = calculate_emissions(activity)
    print_result(result)


def demo_hospitality():
    """Demo 3: Hotel chain"""
    print("\n[DEMO 3] Hospitality Chain (100 rooms)")
    print("-" * 60)

    activity = ActivityData(
        company_name="Luxury Hotel",
        industry="Hospitality",
        lpg_kg=1000,                     # Hot water, kitchen
        electricity_kwh=100000,          # AC, lighting, cooking
        flights_domestic_km=30000,
        employee_commute_car_km=100000,
        waste_landfill_kg=5000,          # Guest waste
    )

    result = calculate_emissions(activity)
    print_result(result)


def demo_comparison():
    """Demo 4: Side-by-side comparison"""
    print("\n[DEMO 4] Company Comparison")
    print("-" * 60)

    companies = [
        ("Small Office", ActivityData(
            electricity_kwh=10000,
            employee_commute_car_km=20000,
        )),
        ("Medium Corp", ActivityData(
            electricity_kwh=100000,
            diesel_litres=500,
            employee_commute_car_km=200000,
            flights_domestic_km=10000,
        )),
        ("Large Enterprise", ActivityData(
            electricity_kwh=500000,
            diesel_litres=2000,
            natural_gas_m3=1000,
            employee_commute_car_km=500000,
            flights_domestic_km=50000,
            flights_international_km=100000,
            waste_landfill_kg=10000,
            supply_chain_spend_inr=100000000,
        )),
    ]

    results = []
    for name, activity in companies:
        result = calculate_emissions(activity)
        results.append((name, result))
        print(f"{name:20} => {result.total_tco2e:>8.2f} tCO2e")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SWACH AI CARBON AGENT - CALCULATOR DEMO")
    print("="*60)

    # Run all demos
    demo_small_startup()
    demo_manufacturing()
    demo_hospitality()
    demo_comparison()

    print("\n[SUCCESS] Demo complete!")
    print("\nTo use the calculator in your code:")
    print("  from tools.calculator import ActivityData, calculate_emissions")
    print("  activity = ActivityData(electricity_kwh=50000, ...)")
    print("  result = calculate_emissions(activity)")
    print("  print(result.total_tco2e)  # tonnes CO2 equivalent")

