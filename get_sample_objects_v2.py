from dataclasses import dataclass
from sources.locations import IMAGE_PARENT_FOLDER
import myimgfuncs
import myocrfuncs
from myocrfuncs import REGIONS, ImageObject
import os
import cv2
from pprint import pprint
from database.db import Database

db = Database()

OUTPUT_FOLDER = "regions/"
if not os.path.isdir(OUTPUT_FOLDER):
    os.mkdir(OUTPUT_FOLDER)


def get_objects(src, show=False):
    try:
        img = cv2.imread(src)
        top_row = img[:100]
        clean = myimgfuncs.denoise(top_row)

        return myocrfuncs.get_top_objects(clean)

    except Exception as e:
        print(f"Error... source path {src}")
        print(e)
        try:
            input("Press enter to coninue (or ctrl-c to kill)\n")
        except KeyboardInterrupt:
            raise(e)


# return the first and last record from each volume
def get_head_and_tail(vol: str) -> tuple[str, str]:
    fullpath = os.path.join(IMAGE_PARENT_FOLDER, vol)
    paths = sorted(os.scandir(fullpath), key=lambda path: path.name)

    return (paths[0], paths[-2])  # -2 as last doc will be back page


# iterate through source images
volumes = db.get_vols()
for vol, first, last in volumes:
    print(vol)
    path_head, path_tail = get_head_and_tail(vol)
    objs_head = get_objects(path_head, True)
    objs_tail = get_objects(path_tail, True)
    break