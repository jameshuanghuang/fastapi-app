from fastapi import APIRouter
from app.models.option import Option

router = APIRouter()

@router.post("/predict")
async def predict(option: Option):
    return {"type": option.type, "prediction": option.S0}

@router.post("/prime")
async def prime(num: int):
    """ guess if the number pass in is prime or not """
    if num < 2:
        return {"is_prime": False}
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return {"is_prime": False}
    return {"is_prime": True}