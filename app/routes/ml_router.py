import asyncio
from fastapi import APIRouter
from app.models.option import Option

router = APIRouter()

@router.post("/predict")
async def predict(option: Option):
    return {"type": option.type, "prediction": option.S0}

@router.post("/prime")
async def prime(num: int):
    latest_checked = None  # Track the latest divisor checked

    async def is_prime(n):
        nonlocal latest_checked
        if n < 2:
            return {"is_prime": False, "completed": True}
        elif n == 2 or n == 3:
            return {"is_prime": True, "completed": True}
        elif n % 2 == 0 or n % 3 == 0:
            return {"is_prime": False, "completed": True}

        sqrt_n = int(n**0.5)
        k = 1
        while (6 * k - 1) <= sqrt_n:
            if n % (6 * k - 1) == 0 or n % (6 * k + 1) == 0:
                return {"is_prime": False, "completed": True, "num_checked": 6 * k + 1}
            latest_checked = 6 * k + 1
            k += 1
            await asyncio.sleep(0)  # Allow other tasks to run
        return {"is_prime": True, "completed": True, "num_checked": latest_checked}

    try:
        return await asyncio.wait_for(is_prime(num), timeout=2.5)
    except asyncio.TimeoutError:
        return {"is_prime": None, "completed": False, "latest_checked": latest_checked}