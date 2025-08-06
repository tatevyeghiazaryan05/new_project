from fastapi import FastAPI

from api.endpoints import images
from api.endpoints import products_crud
from api.endpoints import qr_stats
app = FastAPI()


@app.get("/")
def get():
    return "a"


app.include_router(images.image_router)
app.include_router(products_crud.products_router)
app.include_router(qr_stats.qr_stats_router)
