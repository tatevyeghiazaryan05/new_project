from datetime import date

from fastapi import APIRouter
from services.statistics import StatsService

statistics_router = APIRouter()
statistics_service = StatsService()


@statistics_router.get("/api/scan")
def scan_data_to_db():
    return statistics_service.scan_data_to_db()


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


@statistics_router.get("/stats/period/{start_date}/{end_date}")
def stats_period(start_date: date, end_date: date):
    return statistics_service.get_stats_for_period(start_date, end_date)
