import cv2
from numpy import ndarray
import os
import pytesseract
import re

import myimgfuncs
from sources.locations import IMAGE_PARENT_FOLDER
from database.db import Database
from myocrfuncs import DIGITS

db = Database()

# return the first and last record from each volume
def get_head_and_tail(vol: str) -> tuple[str, str]:
    fullpath = os.path.join(IMAGE_PARENT_FOLDER, vol)
    paths = sorted(os.scandir(fullpath), key=lambda path: path.name)

    return (paths[0], paths[-2])  # -2 as last doc will be back page


def get_vol_paths(vol: str) -> list[str]:
    fullpath = os.path.join(IMAGE_PARENT_FOLDER, vol)
    paths = sorted(os.scandir(fullpath), key=lambda path: path.name)

    return paths


def get_service_no_img(filename: str) -> ndarray:
    img = cv2.imread(filename)
    red = img[30:60, 185:385,2]
    scaled = myimgfuncs.resize(red)
    thresh = cv2.threshold(scaled, 200, 255, cv2.THRESH_BINARY_INV)[1]
    clean = myimgfuncs.denoise(thresh)

    return clean


# iterate through source images - we only care about service no right now
volumes = db.get_vols()
for vol, first, last in volumes:
    paths = get_vol_paths(vol)
    for fp in paths:
        img = get_service_no_img(fp)
        myimgfuncs.show_img(img)
        # use mode 8 (single word) instead of 7
        service_no = pytesseract.image_to_string(img, config=f"--psm 8 {DIGITS}")
        print(service_no)
        results = db.find_service_no(service_no)
        if len(results) == 1:
            print("Hit", service_no)
        if len(results) > 1:
            print(f"SKIPPED - found multiple records for service no {service_no}")
            continue
