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
        objs = []
        for region in REGIONS:
            img = myimgfuncs.load_snip(src, region.rect)
            #bounding_box = myimgfuncs.find_bounding_box(img, True)
            #img = myimgfuncs.snip_image(img, bounding_box)
            img = myimgfuncs.clean(img)
            if show:
                myimgfuncs.show_img(img, src.name)
            #img = myimgfuncs.upscale(img)
            #boxes = myocrfuncs.get_character_boxes(img)
            obj = myocrfuncs.get_region_object(img, region)
            #obj = ImageObject(region, img, boxes)
            objs.append(obj)

        return objs

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