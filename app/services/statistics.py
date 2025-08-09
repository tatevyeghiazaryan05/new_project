import datetime
from datetime import datetime, date, timedelta

from db_connection import DbConnection


class StatsService:
    def __init__(self):
        self.db = DbConnection()

    def scan_data_to_db(self):
        self.db.cursor.execute("""INSERT INTO scan_events (created_at) VALUES (NOW())""")
        self.db.conn.commit()

    def get_total_scans(self):
        """Returns total scan counts grouped by app_name."""
        self.db.cursor.execute("""SELECT COUNT(*) as total FROM scan_events""")
        return self.db.cursor.fetchall()

    def get_total_scans_by_date(self):
        """Returns daily scan counts."""
        self.db.cursor.execute("""
            SELECT TO_CHAR(created_at, 'YYYY-MM-DD') AS date, COUNT(*) AS total
            FROM scan_events
            GROUP BY date
            ORDER BY date
        """)
        return self.db.cursor.fetchall()

    def get_scan_counts_by_hour(self):
        self.db.cursor.execute("""SELECT created_at from scan_events""")
        timestamps = self.db.cursor.fetchall()

        hour_counts = {}

        for t in timestamps:
            dt = datetime.strptime(str(dict(t).get("created_at")), "%Y-%m-%d %H:%M:%S.%f")
            hour = dt.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1

        return [{"hour": hour, "count": hour_counts[hour]} for hour in sorted(hour_counts)]

    def get_average_scans_per_day(self):
        self.db.cursor.execute("""SELECT AVG(daily_count) AS average_per_day FROM 
                                (SELECT DATE(created_at) AS day, COUNT(*) AS daily_count
                                FROM scan_events GROUP BY day) AS daily_counts""")
        result = self.db.cursor.fetchone()
        return {"average_scans_per_day": float(result['average_per_day']) if result['average_per_day'] else 0.0}

    def get_stats_for_period(self, start_date: date, end_date: date):
        end_date = end_date + timedelta(days=1)
        if start_date is None or end_date is None:
            raise ValueError("Invalid input")

        self.db.cursor.execute("""SELECT TO_CHAR(created_at, 'YYYY-MM-DD') AS date,
                                COUNT(*) AS total FROM scan_events
                                WHERE created_at >= %s AND created_at <= %s
                                GROUP BY date ORDER BY date""", (start_date, end_date))
        return self.db.cursor.fetchall()
