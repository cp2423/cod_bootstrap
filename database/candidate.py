from dataclasses import dataclass
from datetime import datetime, timedelta
from jaro import jaro_winkler_metric as jw
from db import CWGC_SCHEMA as schema
from ..record import RecordFrontPage


CWGC_DATE_FORMAT = "%d-%m-%Y"
RECORD_DATE_FORMAT = "%d-%m-%y"

@dataclass
class Candidate:
    score: int = 0
    record: RecordFrontPage
    row: tuple

    def score(self):
        scores = [
            self._score_surname(),
            self._score_date(),
            self._score_unit()
        ]
        return sum(scores) / len(scores)


    def _score_date(self):
        date0 = datetime.strptime(self.record.date, RECORD_DATE_FORMAT) - timedelta()
        # handle "17" -> "1917" not "2017"
        date0 = datetime(date0.year - 100, date0.month, date0.day)
        date1 = datetime.strptime(self.row[schema.DATE_OF_DEATH], CWGC_DATE_FORMAT)
        date2 = datetime.strptime(self.row[schema.DATE_OF_DEATH_2], CWGC_DATE_FORMAT)

        if date0 == date1:
            return 1
        elif date0 == date2:
            return 1
        else:
            # TODO something more sophisticated here?
            return 0


    def _score_surname(self):
        return jw(self.record.surname, self.row[schema.SURNAME]),


    def _score_unit(self):
        pass