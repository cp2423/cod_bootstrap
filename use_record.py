import os
from lookup import lookup
from record import Record

FOLDER = "/Users/chris/Dev/cod_records/aws/extracted/"


for fp in os.scandir(FOLDER):
    if not fp.is_dir():
        continue
    images = [fp for fp in os.scandir(fp) if fp.name.endswith(".jpg")]
    images.sort(key=lambda fp: fp.name)
    pairs = [(images[i], images[i+1]) for i in range(0, len(images), 2)]

    for front, back in pairs:
        r = Record(front.path, back.path)
        lookup(r)
        break