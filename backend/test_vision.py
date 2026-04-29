import os
from dotenv import load_dotenv
from tools.vision_analyzer import UtilityBillAnalyzer

load_dotenv()

analyzer = UtilityBillAnalyzer()

print("Testing Electricity-Bill.png...")
result1 = analyzer.analyze_bill("assets/Electricity-Bill.png", "electricity")
print("Result 1:")
print(result1)
print("-" * 50)

print("Testing npl_current_bill.jpg...")
result2 = analyzer.analyze_bill("assets/npl_current_bill.jpg", "electricity")
print("Result 2:")
print(result2)
