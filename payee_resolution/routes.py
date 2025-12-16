from fastapi import APIRouter, Query
from .models import RealPayeeNameResponse
from .logic import identify_real_payee

router = APIRouter()

@router.get("/payees/real-name", response_model=RealPayeeNameResponse)
async def get_real_payee_name(
    payee: str = Query(..., description="Raw payee description")
):
    """
    Returns the standardized real payee name for a given raw payee string.
    """
    real_name, confidence = identify_real_payee(payee)
    return RealPayeeNameResponse(real_name=real_name, confidence=confidence)
