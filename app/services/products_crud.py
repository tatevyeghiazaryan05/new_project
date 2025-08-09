import datetime

from fastapi import HTTPException, status

from app.db_connection import DbConnection


class Products:
    def __init__(self):
        self.db = DbConnection()

    def get_home_page_products(self):
        try:
            self.db.cursor.execute("""INSERT INTO scan_time (created_at) VALUES (%s)""",
                                   (datetime.datetime.now(),))
            self.db.conn.commit()
        except Exception:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Error inserting scan time")
