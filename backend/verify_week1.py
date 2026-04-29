#!/usr/bin/env python
"""
Week 1 System Verification Script
Checks if all 4 tools and agent are working
"""

print('='*70)
print('SWACH AI CARBON AGENT - WEEK 1 VERIFICATION')
print('='*70)

# Test all imports
tests = []

try:
    from tools import calculate_emissions, ActivityData
    tests.append(('Tool 1: GHG Calculator', True, None))
    print('\n[OK] Tool 1: GHG Calculator imported')
except Exception as e:
    tests.append(('Tool 1: GHG Calculator', False, str(e)))
    print(f'\n[FAIL] Tool 1: {e}')

try:
    from tools import search_carbon_offsets
    tests.append(('Tool 2: Tavily Search', True, None))
    print('[OK] Tool 2: Tavily Search imported')
except Exception as e:
    tests.append(('Tool 2: Tavily Search', False, str(e)))
    print(f'[FAIL] Tool 2: {e}')

try:
    from tools import retrieve_ghg_knowledge
    tests.append(('Tool 3: ChromaDB Retriever', True, None))
    print('[OK] Tool 3: ChromaDB Retriever imported')
except Exception as e:
    tests.append(('Tool 3: ChromaDB Retriever', False, str(e)))
    print(f'[FAIL] Tool 3: {e}')

try:
    from tools import generate_pdf_report
    tests.append(('Tool 4: PDF Generator', True, None))
    print('[OK] Tool 4: PDF Generator imported')
except Exception as e:
    tests.append(('Tool 4: PDF Generator', False, str(e)))
    print(f'[FAIL] Tool 4: {e}')

try:
    from langchain.agents import create_react_agent, AgentExecutor
    tests.append(('LangChain ReAct', True, None))
    print('[OK] LangChain ReAct Agent imported')
except Exception as e:
    tests.append(('LangChain ReAct', False, str(e)))
    print(f'[FAIL] LangChain: {e}')

# Quick functional test
print('\n' + '-'*70)
print('FUNCTIONAL TEST')
print('-'*70)

try:
    from tools import calculate_emissions, ActivityData
    activity = ActivityData(electricity_kwh=10000, diesel_litres=100)
    result = calculate_emissions(activity)
    tests.append((f'Calculator Test ({result.total_tco2e} tCO2e)', True, None))
    print(f'[OK] Calculator: {result.total_tco2e} tCO2e')
except Exception as e:
    tests.append(('Calculator Test', False, str(e)))
    print(f'[FAIL] Calculator: {e}')

# Summary
print('\n' + '='*70)
passed_count = sum(1 for _, p, _ in tests if p)
total_count = len(tests)
print(f'VERIFICATION COMPLETE: {passed_count}/{total_count} tests passed')
print('='*70)

if passed_count == total_count:
    print('\n✓ ALL SYSTEMS OPERATIONAL - READY FOR WEEK 2')
else:
    print('\n! SOME COMPONENTS NEED ATTENTION')
