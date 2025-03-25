# main.py
import uvicorn
from fastapi import FastAPI
from infrastructure.routes.product_routes import router as product_router
from infrastructure.routes.auth_routes import router as auth_router

app = FastAPI()

app.include_router(product_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)