import datetime
from datetime import datetime

from db_connection import DbConnection


class QRStatsService:
    def __init__(self):
        self.db = DbConnection()

    def save_scan(self, app_name: str, user_agent: str):
        self.db.cursor.execute(
            """
            INSERT INTO scan_events (app_name, user_agent, created_at)
            VALUES (%s, %s, %s)
            """,
            (app_name, user_agent, datetime.datetime.now())
        )
        self.db.conn.commit()

    def get_stats(self):
        self.db.cursor.execute("""
            SELECT app_name, COUNT(*) as total
            FROM scan_events
            GROUP BY app_name
        """)

        total_by_app = self.db.cursor.fetchall()

        self.db.cursor.execute("""
                    SELECT TO_CHAR(created_at, 'YYYY-MM-DD') AS date, COUNT(*) AS total
                    FROM scan_events
                    GROUP BY date
                    ORDER BY date
                """)
        daily_trend = self.db.cursor.fetchall()

        return {
            "by_app": total_by_app,
            "daily_trend": daily_trend
        }

    def get_count_of_log_in_date(self):
        self.db.cursor.execute("""SELECT created_at from scan_events""")
        created_at = self.db.cursor.fetchall()

        hour_counts = {}

        for t in created_at:
            dt = datetime.strptime(str(dict(t).get("created_at")), "%Y-%m-%d %H:%M:%S.%f")

            hour_counts[dt.hour] = hour_counts.get(dt.hour, 0) + 1

        for hour in sorted(hour_counts):
            print(f"Hour {hour}: {hour_counts[hour]}")
