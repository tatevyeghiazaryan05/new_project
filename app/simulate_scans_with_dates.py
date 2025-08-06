import requests
import random
import time
import datetime
import psycopg2

BASE_URL = "http://127.0.0.1:8000/api/success/image"

# PostgreSQL connection settings
DB_SETTINGS = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "password",
    "database": "newproject"
}

# Sample User-Agent headers for different apps/browsers
user_agents = [
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) Instagram 150.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) WhatsApp/2.21.100",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Facebook/150.0.0.0",
    "Mozilla/5.0 (Linux; Android 10; Pixel 4) Chrome/90.0.0.0 Mobile",
]


def insert_backdated_scan(app_name, user_agent, days_ago):
    """Insert a scan event into the DB with a specific date."""
    scan_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)

    conn = psycopg2.connect(**DB_SETTINGS)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scan_events (app_name, user_agent, created_at)
        VALUES (%s, %s, %s)
    """, (app_name, user_agent, scan_date))
    conn.commit()
    conn.close()


def simulate_api_scans(count=5, delay=0.5):
    """Call the API endpoint to create real-time scans."""
    for i in range(count):
        ua = random.choice(user_agents)
        print(f"[API] Scan {i+1}/{count} from: {ua}")
        response = requests.get(BASE_URL, headers={"User-Agent": ua})
        print(f"Status: {response.status_code}")
        time.sleep(delay)


def simulate_backdated_scans(days=7, scans_per_day=3):
    """Insert fake scans for previous days."""
    for d in range(days, 0, -1):
        for _ in range(scans_per_day):
            ua = random.choice(user_agents)
            app_name = detect_app_name(ua)
            insert_backdated_scan(app_name, ua, days_ago=d)
        print(f"[DB] Inserted {scans_per_day} scans for {d} days ago.")


def detect_app_name(user_agent):
    """Guess app from User-Agent."""
    ua_lower = user_agent.lower()
    if "instagram" in ua_lower:
        return "Instagram"
    elif "whatsapp" in ua_lower:
        return "WhatsApp"
    elif "facebook" in ua_lower:
        return "Facebook"
    return "Other"


if __name__ == "__main__":
    # Simulate real scans now
    simulate_api_scans(count=5, delay=0.2)

    # Insert fake past scans
    simulate_backdated_scans(days=7, scans_per_day=4)

    print("\n✅ Simulation complete! Check: http://127.0.0.1:8000/api/scan-count")
