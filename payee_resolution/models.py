from pydantic import BaseModel

class RealPayeeNameResponse(BaseModel):
    real_name: str
    confidence: float
