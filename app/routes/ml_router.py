from fastapi import APIRouter
from app.models.option import Option

router = APIRouter()

@router.post("/predict")
async def predict(option: Option):
    return {"type": option.type, "prediction": option.S0}