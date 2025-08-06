from fastapi import APIRouter
from services.qr_stats import QRStatsService

products_router = APIRouter()
stats_service = QRStatsService()


@products_router.get("/api/scan-count")
def get_scan_count():
    return stats_service.get_stats()

