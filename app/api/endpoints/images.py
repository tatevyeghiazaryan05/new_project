from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from services.statistics import StatsService

image_router = APIRouter()
stats_service = StatsService()


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
    stats_service.save_scan(app_name, user_agent)

    return FileResponse("./images/successfully_pic.jpg")
