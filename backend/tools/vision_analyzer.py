"""
Vision Analyzer Tool for Swach AI Carbon Agent

Uses LLM Vision capabilities (Gemini 1.5 Flash) to analyze uploaded utility bills,
invoices, and documents to extract activity data (kWh, litres, costs).
"""

import os
import json
import logging
import requests
import base64
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UtilityBillAnalyzer:
    """Analyzes utility bills to extract carbon footprint activity data"""

    def __init__(self, model: str = "gemini-2.5-flash"):
        """Initialize the vision analyzer"""
        self.model_name = model
        self.api_key = os.getenv("GEMINI_API_KEY")

    def analyze_bill(self, image_path: str, bill_type: str = "electricity") -> str:
        """
        Analyze an image of a utility bill and extract structured data.
        """
        if not self.api_key:
            return json.dumps({"error": "GEMINI_API_KEY not found in environment."})
            
        if not os.path.exists(image_path):
            return json.dumps({"error": f"Image file not found: {image_path}"})
            
        try:
            with open(image_path, "rb") as image_file:
                # Get mime type based on extension
                ext = image_path.lower().split('.')[-1]
                mime_type = f"image/{ext}" if ext in ['png', 'jpeg', 'webp', 'heic', 'heif'] else "image/jpeg"
                if ext == 'jpg': mime_type = "image/jpeg"
                
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                
            prompts = {
                "electricity": "Extract the following details from this electricity bill: company name, billing period (start and end dates), total electricity consumed in kWh, and total cost in INR. Return ONLY valid JSON format with keys: company_name, billing_period, electricity_kwh, total_cost_inr.",
                "fuel": "Extract the following details from this fuel invoice: company name, date, fuel type (diesel, petrol, etc), quantity in litres, and total cost in INR. Return ONLY valid JSON format with keys: company_name, date, fuel_type, quantity_litres, total_cost_inr.",
                "water": "Extract the following details from this water bill: company name, billing period, total water consumed in cubic meters (m3), and total cost in INR. Return ONLY valid JSON format with keys: company_name, billing_period, water_m3, total_cost_inr."
            }
            
            prompt_text = prompts.get(bill_type.lower(), prompts["electricity"])
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            
            payload = {
                "contents": [{
                    "parts": [
                        {"text": prompt_text},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": encoded_string
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.0,
                    "response_mime_type": "application/json"
                }
            }
            
            logger.info(f"Analyzing {bill_type} bill: {image_path} with {self.model_name}")
            response = requests.post(url, json=payload, headers={"Content-Type": "application/json"})
            
            if response.status_code != 200:
                return json.dumps({"error": f"API Error {response.status_code}: {response.text}"})
                
            resp_data = response.json()
            if "candidates" not in resp_data or not resp_data["candidates"]:
                return json.dumps({"error": "No response generated from Gemini"})
                
            content = resp_data["candidates"][0]["content"]["parts"][0]["text"]
            
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
                
            content = content.strip()
            
            # Validate JSON
            json.loads(content)
            
            return content
            
        except Exception as e:
            logger.error(f"Error analyzing bill: {e}")
            return json.dumps({"error": str(e)})

# Expose functional interface for Langchain tools
def analyze_utility_bill(image_path: str, bill_type: str = "electricity") -> str:
    """
    Tool function to extract consumption data from utility bill images.
    """
    analyzer = UtilityBillAnalyzer()
    return analyzer.analyze_bill(image_path, bill_type)
