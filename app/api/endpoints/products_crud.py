from fastapi import APIRouter
from services.statistics import StatsService

products_router = APIRouter()


@products_router.get("/api/scan-count")
def get_scan_count():
    # Adjust to a defined method; returning total scans as a proxy
    return StatsService().get_total_scans()

