import sqlite3
from record import Record

class CWGC_SCHEMA:
    CWGC_ID = 0
    SURNAME = 1
    FORENAMES = 2
    INTIALS = 3
    AGE_AT_DEATH = 4
    HONOURS = 5
    DATE_OF_DEATH = 6
    DATE_OF_DEATH_2 = 7
    RANK = 8
    REGIMENT = 9
    SECONDARY_REGIMENT = 10
    UNIT = 11
    SECONDARY_UNIT = 11
    COUNTRY_OF_SERVICE = 12
    SERVICE_NO = 13
    BURIAL = 14
    CEMETERY = 15
    GRAVE_REF = 16
    ADDITIONAL_INFO = 17


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

        cur = self.con.execute(sql, params)
        return cur.fetchall()



    def find_service_no(self, service_no: str) -> tuple:
        # cwgc download has each service no wrapped in single quotes
        #service_no = f"'{service_no}'"
        sql = "select * from cwgc where ServiceNumber = ?"
        return self._query(sql, service_no)


    def find_vol(self, vol: str):
        sql = "select * from volumes where vol = ?"
        return self._query(sql, vol)


    def get_vols(self):
        sql = "select * from volumes"
        return self._query(sql)


    # TODO
    # REMOVE THIS IN FUTURE....
    def find_candidates(self, record: Record):
        r = record.front
        sql_stubs = [
            ("ServiceNumber", r.service_no_all),
            ("ServiceNumber", r.service_no_digits),
            ("Rank", r.rank),
            ("Surname", r.surname),
            # ignore forename - too many possible issues
            ("Unit", r.unit),
            ("DateOfDeath", r.date)
        ]

        candidates = []
        flattened = [[(col, val) for val in values] for col, values in sql_stubs]

        with self.con as con:
            for param_pairs in flattened:
                for pair in param_pairs:
                    cur = con.execute("select * from cwgc where ? = ?", pair)
                    candidates += cur.fetchall()

        return candidates


    def search_service_no(self, service_no: str) -> tuple[Record, int]:
        rows = self._find_service_no(service_no)


    def store_match(self, cwgc_id: str, record: Record, match_str: str, score: int) -> int:
        sql = "insert into matches values (?, ?, ?, ?, ?)"
        params = (cwgc_id, match_str, score, record.front.fp, record.back.fp)

        # use context manager to actually COMMIT each time
        with self.con as con:
            cur = con.execute(sql, params)

        return cur.rowcount
