from fastapi import FastAPI
from routers import r_product, r_order

app = FastAPI()

app.include_router(r_product.router, prefix='/products', tags=['Products'])
app.include_router(r_order.router, prefix='/orders', tags=['Orders'])


