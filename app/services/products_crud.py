import datetime

from fastapi import HTTPException, status

from db_connection import DbConnection


class Products:
    def __init__(self):
        self.db = DbConnection()

    def get_home_page_products(self):
        try:
            self.db.cursor.execute("""INSERT INTO scan_time (created_at) VALUES (%s)""",
                                   (datetime.datetime.now()))

            self.db.conn.commit()
            return []
        except Exception as e:
            print("Actual DB Error:", repr(e))
