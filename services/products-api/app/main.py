from fastapi import FastAPI

app = FastAPI()
PRODUCTS = [{"id": 1, "name": "Product 1", "price": 19.99}, 
            {"id": 2, "name": "Product 2", "price": 29.99}]

@app.get("/health")
async def get_health():
    return {"status": "ok"}


@app.get("/products")
async def get_products():
    return PRODUCTS