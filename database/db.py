import sqlite3


class DatabaseMeta(type):
    _instance = None
    _DB = "database/data.db"

    def __call__(cls):
        if cls._instance is None:
            cls._instance = super().__call__()
            # this approach will *not* create a new DB file if it does not already exist
            cls.con = sqlite3.connect(f"file:{cls._DB}?mode=rw", uri=True)

        return cls._instance


class Database(metaclass=DatabaseMeta):
    def _query(self, sql, params=[]):
        # hack to avoid having to remember how to use single item tuples
        if params and type(params) is not tuple:
            params = (params,)
        with self.con as con:
            res = con.execute(sql, params)

            return res.fetchone()


    def find_service_no(self, service_no: str):
        # cwgc download has each service no wrapped in single quotes
        service_no = f"'{service_no}'"
        sql = "select * from cwgc where ServiceNumber = ?"

        return self._query(sql, service_no)


    def find_vol(self, vol: str):
        sql = "select * from volumes where vol = ?"

        return self._query(sql, vol)


    def get_vols(self):
        sql = "select * from volumes"

        return self._query(sql)