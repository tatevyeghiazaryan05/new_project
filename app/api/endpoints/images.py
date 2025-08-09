from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from app.services.statistics import StatsService

image_router = APIRouter()


@image_router.get("/api/success/image")
def success(request: Request):
    user_agent = request.headers.get("user-agent", "Unknown")

    # Detect app from user agent
    app_name = "Other"
    ua_lower = user_agent.lower()
    if "instagram" in ua_lower:
        app_name = "Instagram"
    elif "whatsapp" in ua_lower:
        app_name = "WhatsApp"
    elif "facebook" in ua_lower:
        app_name = "Facebook"

    # Save scan in DB
    # Replaced with an insert-only call since save_scan is not defined
    StatsService().scan_data_to_db()

    return FileResponse("./images/successfully_pic.jpg")
