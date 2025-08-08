from fastapi import APIRouter, Depends
from services.statistics import StatsService

statistics_router = APIRouter()
statistics_service = StatsService()


@statistics_router.post("/api/scan")
def save_scan():
    return statistics_service.save_scan()


@statistics_router.get("/total/scans")
def total_scans():
    return statistics_service.get_total_scans()


@statistics_router.get("/total/scans/by/date")
def total_scans_by_date():
    return statistics_service.get_total_scans_by_date()


@statistics_router.get("/stats/peak-hours")
def peak_scan_hours():
    return statistics_service.get_scan_counts_by_hour()


@statistics_router.get("/stats/average-per-day")
def average_scans_per_day():
    return statistics_service.get_average_scans_per_day()
