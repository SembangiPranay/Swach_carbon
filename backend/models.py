"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from enum import Enum


class ActivityDataRequest(BaseModel):
    """Request model for carbon calculation"""
    company_name: str = Field(..., min_length=1, max_length=200)
    industry: str = Field(default="Unknown")
    employee_count: int = Field(default=1, ge=1)
    
    diesel_litres: float = Field(default=0, ge=0)
    petrol_litres: float = Field(default=0, ge=0)
    natural_gas_m3: float = Field(default=0, ge=0)
    lpg_kg: float = Field(default=0, ge=0)
    coal_tonnes: float = Field(default=0, ge=0)
    
    electricity_kwh: float = Field(default=0, ge=0)
    
    flights_km: float = Field(default=0, ge=0)
    waste_kg: float = Field(default=0, ge=0)
    water_m3: float = Field(default=0, ge=0)
    commute_km: float = Field(default=0, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "company_name": "TechCorp India",
                "industry": "Technology",
                "employee_count": 500,
                "diesel_litres": 500,
                "petrol_litres": 200,
                "natural_gas_m3": 100,
                "lpg_kg": 100,
                "coal_tonnes": 0,
                "electricity_kwh": 10000,
                "flights_km": 2000,
                "waste_kg": 500,
                "water_m3": 1000,
                "commute_km": 5000
            }
        }


class CalculationResponse(BaseModel):
    """Response for POST /calculate"""
    calculation_id: str = Field(..., description="UUID for tracking this calculation")


class StreamEventType(str, Enum):
    THOUGHT = "thought"
    ACTION = "action"
    OBSERVATION = "observation"
    PROGRESS = "progress"
    COMPLETE = "complete"
    ERROR = "error"


class StreamEvent(BaseModel):
    """Event streamed via SSE"""
    type: StreamEventType
    content: str
    timestamp: Optional[str] = None


class CalculationResult(BaseModel):
    """Complete calculation result"""
    scope1_kg: float
    scope2_kg: float
    scope3_kg: float
    total_tco2e: float
    breakdown: Dict[str, float]


class ReportMetadata(BaseModel):
    """Metadata about a generated report"""
    calculation_id: str
    company_name: str
    total_tco2e: float
    generated_at: str
    status: str  # "ready" or "pending"


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    services: Dict[str, str] = Field(
        default_factory=lambda: {
            "groq": "checking",
            "tavily": "checking",
            "gemini": "checking",
            "database": "checking"
        }
    )


class ErrorResponse(BaseModel):
    """Standard error response"""
    error: str
    detail: Optional[str] = None
    status_code: int
