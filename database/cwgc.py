import sqlite3

DB = "database/data.db"

class Database:
    def __init__(self):
        # this approach will *not* create a new DB file if it does not already exist
        self.conn = sqlite3.connect(f"file:{DB}?mode=rw", uri=True)

    def find(self, service_no: str):
        with self.conn as conn:
            # cwgc download has each service no wrapped in single quotes
            service_no = f"'{service_no}'"
            sql = "select * from cwgc where ServiceNumber = ?"
            res = conn.execute(sql, (service_no,))

            return res.fetchone()