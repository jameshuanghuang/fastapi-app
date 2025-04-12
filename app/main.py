from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import ValidationError
from starlette.websockets import WebSocketDisconnect
from app.services.calc_service import blsprice, calc
from app.models.option import Option
from app.routes import ml_router

app = FastAPI()
app.include_router(ml_router.router, prefix="/ml", tags=["ml"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("app/static/index.html")

@app.get("/blsprice")
async def get_blsprice(S0: float, K: float, T: float, rfr: float, q1: float, sigma: float):
    call_price, put_price = blsprice(S0, K, T, rfr, q1, sigma)
    return {
        "call_price": round(call_price, 2),
        "put_price": round(put_price, 2),
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        try:
            # Receive data from the client
            data = await websocket.receive_json()

            # Validate the data using the Option model
            option = Option(**data)

            # Perform the calculation
            price, table_data = calc(
                S0=option.S0,
                K=option.K,
                sigma=option.sigma,
                rfr=option.rfr,
                T=option.T,
                q1=option.q1,
                opt_type=option.type
            )

            # Send the result back to the client
            result = {
                "type": "result",
                "message": f"{option.type.capitalize()} option price: ${price}",
                "data": table_data,
            }
            await websocket.send_json(result)
        
        # Exit the loop when the client disconnects
        except WebSocketDisconnect:
            break

        except ValidationError as e:
            # Handle validation errors and send error messages to the client
            error_message = {
                "type": "error",
                "message": "Validation error",
                "details": e.errors(),  # List of validation errors
            }
            await websocket.send_json(error_message)