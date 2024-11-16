from database.db import Database, CWGC_SCHEMA as c
import jaro
import re
from record import Record, RecordFrontPage

RATIO_TOLERANCE = 0.8
db = Database()


def _get_clean_service_no(page: RecordFrontPage):
    # check if both versions are empty, would suggest an Officer
    if page.service_no_all == "" and page.service_no_digits == "":
        return None
    # if both versions match nothing else can be done, just pick one
    if page.service_no_all == page.service_no_digits:
        return page.service_no_digits
    # try removing non-digits from all
    all_clean = re.sub("[^0-9]", "", page.service_no_all)
    if all_clean == page.service_no_digits:
        return page.service_no_digits

def lookup(record: Record):
    page = record.front
    # first look for service no
    service_no = _get_clean_service_no(page)
    if service_no:
        res = db.find_service_no(service_no)
        #print(res)
        if len(res) == 0:
            print("!!!!!!!!!!!!!!!! no hit !!!!!!!!!!!!!!!! service no", service_no, page.fp)
        elif len(res) == 1:
            # only one hit, cross reference to check validity
            surname = res[0][c.SURNAME]
            if surname != page.surname:
                ratio = jaro.jaro_winkler_metric(surname, page.surname)
                if ratio < RATIO_TOLERANCE:
                    print(f"*** {page.fp} Bad mismatch on surname: expected {surname} found {page.surname} ratio {ratio}")
        else:
            print("??????????????? multiple hits found ??????????????? service no", service_no, page.fp)
    else:
        print(f"Service no is blank all='{page.service_no_all}' digits='{page.service_no_digits}'", page.fp)