from fastapi import APIRouter
from services.qr_stats import QRStatsService

qr_stats_router = APIRouter()
statistics_service = QRStatsService()


@qr_stats_router.get("/api/log-in/date/count")
def count_of_log_in_date():
    return statistics_service.get_count_of_log_in_date()
