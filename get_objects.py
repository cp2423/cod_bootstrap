from cv2 import imwrite
from locations import IMAGE_TEST_FOLDER
import myimgfuncs
from myimgfuncs import Rectangle
import myocrfuncs
from os import mkdir, scandir
from os.path import isdir
import cv2
from pprint import pprint

OUTPUT_FOLDER = "regions/"
if not isdir(OUTPUT_FOLDER):
    mkdir(OUTPUT_FOLDER)

REGIONS = {
    # NB Rectangle is y1, y2, x1, x2
    "service_no": Rectangle(30, 65, 190, 300),
    "surname": Rectangle(30, 65, 600, 850),
    "unit": Rectangle(100, 139, 200, 400)
}

TESSERACT_OPTIONS = {
    "service_no": myocrfuncs.DIGITS,
    "surname": myocrfuncs.CAPITALS,
    "unit": ""
}


def get_source_images(path: str, extension: str)  -> list[str]:
    return [f.path for f in scandir(path) if f.name.endswith(extension)]



# iterate through source images
sources = get_source_images(IMAGE_TEST_FOLDER, ".jpg")
src_count = 0

for src in sorted(sources):
    # skip even images (back of the page)
    src_count += 1
    if src_count % 2 == 0:
        continue
    try:
        id = str(src_count).zfill(5)
        for (region, rectangle) in REGIONS.items():
            img = myimgfuncs.load_snip(src, rectangle)
            bounding_box = myimgfuncs.find_bounding_box(img)
            img = myimgfuncs.snip_image(img, bounding_box)
            img = myimgfuncs.clean(img)
            #img = myimgfuncs.upscale(img)
            region_filename = f"{OUTPUT_FOLDER}{id}_{region}.png"
            imwrite(region_filename, img)
            print(myocrfuncs.read_text(img, ""))
    except Exception as e:
        print(f"Error... source no {src_count} path {src}")
        print(e)
        input("Press enter to coninue (or ctrl-c to kill)")