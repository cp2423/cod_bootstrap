from cv2 import imwrite
from locations import IMAGE_TEST_FOLDER
import myimgfuncs
from myimgfuncs import Rectangle
from os import mkdir, scandir
from os.path import isdir

OUTPUT_FOLDER = "regions/"
if not isdir(OUTPUT_FOLDER):
    mkdir(OUTPUT_FOLDER)

REGIONS = {
    # NB Rectangle is y1, y2, x1, x2
    "service_no": Rectangle(30, 65, 190, 300),
    "surname": Rectangle(30, 65, 600, 850),
    "unit": Rectangle(100, 139, 200, 400)
}


def get_source_images(path: str, extension: str)  -> list[str]:
    return [f for f in scandir(path) if f.name.endswith(extension)]


# iterate through source images
sources = get_source_images(IMAGE_TEST_FOLDER, ".jpg")
for src in sources:
    for (region, rectangle) in REGIONS.items():
        snip = myimgfuncs.load_snip(src, rectangle)
        #myimgfuncs.show(snip)
        bounding_box = myimgfuncs.find_bounding_box(snip)
        upscaled = myimgfuncs.upscale_region(snip, bounding_box)
        region_filename = OUTPUT_FOLDER + region + ".png"
        imwrite(region_filename, upscaled)
    break