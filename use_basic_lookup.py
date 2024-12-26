import os
from lookup import basic_service_digits_match
from record import Record

START_FILE = "/Users/chris/Dev/cod_records/aws/extracted/31829_B016684/31829_B016684-00218.jpg"

FOLDER = "/Users/chris/Dev/cod_records/aws/extracted/"
FILES = sorted(os.scandir(FOLDER), key=lambda fp: fp.name)

start_vol_i = start_file_i = 0

if START_FILE:
    start_vol, start_fn = START_FILE.split('/')[7:9]
    start_vol_i = [fp.name for fp in FILES].index(start_vol)
    start_file_no = start_fn[14:19]
    start_file_i = int(start_file_no) + 2


for fp in FILES[start_vol_i:]:
    if not fp.is_dir():
        continue

    images = [fp for fp in os.scandir(fp) if fp.name.endswith(".jpg")]
    images.sort(key=lambda fp: fp.name)
    pairs = [(images[i], images[i+1]) for i in range(start_file_i, len(images), 2)]
    matches_count = 0

    for front, back in pairs:
        try:
            record = Record(front.path, back.path)
            matches_count += basic_service_digits_match(record)
        except Exception as e:
            print(front)
            raise(e)

    pct = matches_count / len(pairs)
    print(f"Processed volume {fp}, matches = {matches_count} of {len(pairs)} ({pct:.1%})")