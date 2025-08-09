import datetime
from datetime import datetime, date, timedelta

from db_connection import DbConnection


class StatsService:
    def __init__(self):
        self.db = DbConnection()

    def scan_data_to_db(self):
        try:
            self.db.cursor.execute("""INSERT INTO scan_events (created_at) VALUES (NOW())""")
            self.db.conn.commit()
        except Exception as e:
            print("StatsService.scan_data_to_db error:", repr(e))

    def get_total_scans(self):
        """Returns total scan counts grouped by app_name."""
        try:
            self.db.cursor.execute("""SELECT COUNT(*) as total FROM scan_events""")
            return self.db.cursor.fetchall()
        except Exception as e:
            print("StatsService.get_total_scans error:", repr(e))
            return []

    def get_total_scans_by_date(self):
        """Returns daily scan counts."""
        try:
            self.db.cursor.execute("""
                SELECT TO_CHAR(created_at, 'YYYY-MM-DD') AS date, COUNT(*) AS total
                FROM scan_events
                GROUP BY date
                ORDER BY date
            """)
            return self.db.cursor.fetchall()
        except Exception as e:
            print("StatsService.get_total_scans_by_date error:", repr(e))
            return []

    def get_scan_counts_by_hour(self):
        try:
            self.db.cursor.execute("""SELECT created_at from scan_events""")
            timestamps = self.db.cursor.fetchall()

            hour_counts = {}

            for t in timestamps:
                dt = datetime.strptime(str(dict(t).get("created_at")), "%Y-%m-%d %H:%M:%S.%f")
                hour = dt.hour
                hour_counts[hour] = hour_counts.get(hour, 0) + 1

            return [{"hour": hour, "count": hour_counts[hour]} for hour in sorted(hour_counts)]
        except Exception as e:
            print("StatsService.get_scan_counts_by_hour error:", repr(e))
            return []

    def get_average_scans_per_day(self):
        try:
            self.db.cursor.execute("""SELECT AVG(daily_count) AS average_per_day FROM 
                                    (SELECT DATE(created_at) AS day, COUNT(*) AS daily_count
                                    FROM scan_events GROUP BY day) AS daily_counts""")
            result = self.db.cursor.fetchone()
            return {"average_scans_per_day": float(result['average_per_day']) if result['average_per_day'] else 0.0}
        except Exception as e:
            print("StatsService.get_average_scans_per_day error:", repr(e))
            return {"average_scans_per_day": 0.0}

    def get_stats_for_period(self, start_date: date, end_date: date):
        try:
            if start_date is None or end_date is None:
                print("StatsService.get_stats_for_period error: Invalid input")
                return []

            end_date_inclusive = end_date + timedelta(days=1)
            self.db.cursor.execute("""SELECT TO_CHAR(created_at, 'YYYY-MM-DD') AS date,
                                    COUNT(*) AS total FROM scan_events
                                    WHERE created_at >= %s AND created_at <= %s
                                    GROUP BY date ORDER BY date""", (start_date, end_date_inclusive))
            return self.db.cursor.fetchall()
        except Exception as e:
            print("StatsService.get_stats_for_period error:", repr(e))
            return []

    def get_year_over_year_percentage_increase(self):
        try:
            # Current year total
            self.db.cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM scan_events
                WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW())
                """
            )
            current_row = self.db.cursor.fetchone()
            current_total = int(current_row["total"]) if current_row and current_row.get("total") is not None else 0

            # Last year total
            self.db.cursor.execute(
                """
                SELECT COUNT(*) AS total
                FROM scan_events
                WHERE EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM NOW()) - 1
                """
            )
            last_row = self.db.cursor.fetchone()
            last_total = int(last_row["total"]) if last_row and last_row.get("total") is not None else 0

            if last_total == 0:
                percentage_increase = 0.0 if current_total == 0 else 100.0
            else:
                percentage_increase = ((current_total - last_total) / last_total) * 100.0

            return {
                "current_year_total": current_total,
                "last_year_total": last_total,
                "percentage_increase": float(percentage_increase),
            }
        except Exception as e:
            print("StatsService.get_year_over_year_percentage_increase error:", repr(e))
            return {"current_year_total": 0, "last_year_total": 0, "percentage_increase": 0.0}
