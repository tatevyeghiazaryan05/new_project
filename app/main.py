from fastapi import FastAPI

from api.endpoints import products_crud
from api.endpoints import statistics
app = FastAPI()



app.include_router(products_crud.products_router)
app.include_router(statistics.statistics_router)
