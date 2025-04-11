from pydantic import BaseModel, Field
from typing import Literal

class Option(BaseModel):
    S0: float = Field(..., gt=0, description="Spot price must be greater than 0")
    K: float = Field(..., ge=0, description="Strike price must be greater than 0")
    sigma: float = Field(..., gt=0, description="Volatility must be greater than 0")
    rfr: float = Field(..., ge=0, description="Risk-free rate must be non-negative")
    T: float = Field(..., ge=0, description="Time to maturity must be greater than 0")
    q1: float = Field(..., ge=0, description="Dividend yield must be non-negative")
    type: Literal["call", "put"]  # Option type (call or put)
