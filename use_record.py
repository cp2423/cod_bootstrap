import os

from database.db import Database
from record import Record

db = Database()
FOLDER = "/Users/chris/Dev/cod_records/aws/extracted/"


for (vol, _, _) in db.get_vols():
    path = FOLDER + vol
    images = [fp for fp in os.scandir(path) if fp.name.endswith(".jpg")]
    images.sort(key=lambda fp: fp.name)
    pairs = [(images[i], images[i+1]) for i in range(0, len(images), 2)]

    for front, back in pairs:
        r = Record(front, back)
        break