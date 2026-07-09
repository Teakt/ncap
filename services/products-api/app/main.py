from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
PRODUCTS = [{"id": 1, "name": "Product 1", "price": 19.99}, 
            {"id": 2, "name": "Product 2", "price": 29.99}]

class Product(BaseModel):
    id: int
    name: str
    price: float

@app.get("/health")
async def get_health():
    return {"status": "ok"}


@app.get("/products", response_model=list[Product])
async def get_products():
    return PRODUCTS