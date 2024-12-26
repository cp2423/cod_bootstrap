import os
from lookup import lookup, new_lookup
from record import Record

FOLDER = "/Users/chris/Dev/cod_records/aws/extracted/"


def scan_folders():
    for fp in os.scandir(FOLDER):
        if not fp.is_dir():
            continue
        images = [fp for fp in os.scandir(fp) if fp.name.endswith(".jpg")]
        images.sort(key=lambda fp: fp.name)
        pairs = [(images[i], images[i+1]) for i in range(0, len(images), 2)]

        for front, back in pairs:
            r = Record(front.path, back.path)
            #lookup(r)
            new_lookup(r)
            break


def individual_file(filename):
    fp = FOLDER + filename.split("-")[0] + "/" + filename
    assert os.path.exists(fp)
    r = Record(fp, fp)
    new_lookup(r)

individual_file("31829_B016684-00000.jpg")
#scan_folders()