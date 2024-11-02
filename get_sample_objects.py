from cv2 import imwrite
from sources.locations import IMAGE_PARENT_FOLDER
import myimgfuncs
from myimgfuncs import Rectangle
import myocrfuncs
import os
import cv2
from pprint import pprint
from database.db import Database

db = Database()

OUTPUT_FOLDER = "regions/"
if not os.path.isdir(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)

REGIONS = {
    # NB Rectangle is y1, y2, x1, x2
    "service_no": Rectangle(30, 65, 190, 300),
    "surname": Rectangle(30, 65, 600, 850),
    "forenames": Rectangle(30, 65, 865, 1150)
}

TESSERACT_OPTIONS = {
    "service_no": myocrfuncs.DIGITS,
    "surname": myocrfuncs.CAPITALS,
    "unit": ""
}


def get_objects(vol, src, name):
    try:
        for (region, rectangle) in REGIONS.items():
            img = myimgfuncs.load_snip(src, rectangle)
            bounding_box = myimgfuncs.find_bounding_box(img)
            img = myimgfuncs.snip_image(img, bounding_box)
            img = myimgfuncs.clean(img)
            #img = myimgfuncs.upscale(img)
            # get each letter from region

            # store each letter using name

    except Exception as e:
        print(f"Error... source path {src}")
        print(e)
        input("Press enter to coninue (or ctrl-c to kill)")


# return the first and last record from each volume
def get_top_and_tail(vol: str) -> tuple[str, str]:
    fullpath = os.path.join([IMAGE_PARENT_FOLDER, vol])
    paths = list(os.scandir(fullpath))

    return (paths[0], paths[-2])  # -2 as last doc will be back page


# iterate through source images
volumes = db.get_vols()
for vol, first, last in volumes:
    path0, path-2 = get_top_and_tail(vol)
    get_objects(vol, path0, first)
    get_objects(vol, path-2, last)

