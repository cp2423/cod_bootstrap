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


candidates = [25, 26, 31, 32]

def clean_desperate(img_orig, region):
    count = 0
    _resize = [None, 2, 4]
    _denoise = [True, False]
    _dilate = [True, False]
    _open = [None, (3,3), (5,5)]
    _close = [None, (3,3), (5,5)]

    for resize in _resize:
        for denoise in _denoise:
            for dilate in _dilate:
                for do_open in _open:
                    count += 1
                    if not count in candidates:
                        continue
                    img = img_orig.copy()
                    if resize:
                        size = (img.shape[1] * resize, img.shape[0] * resize)
                        img = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
                    #img = myimgfuncs.get_binary_image(img)
                    if denoise:
                        img = myimgfuncs.denoise(img)
                    if dilate:
                        img = myimgfuncs.dilate(img)
                    if do_open:
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, do_open)
                        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

                    text = myocrfuncs.read_text(img, TESSERACT_OPTIONS[region])
                    results = desperate.get(count, {})
                    results[region] = text
                    results["params"] = {
                        "resize": resize,
                        "denoise": denoise,
                        "dilate": dilate,
                        "open": do_open
                    }
                    desperate[count] = results

                    test_filename = f"{OUTPUT_FOLDER}test_{count}_{region}.png"
                    imwrite(test_filename, img)

# iterate through source images
sources = get_source_images(IMAGE_TEST_FOLDER, ".jpg")
src_count = -1
for src in sorted(sources):
    desperate = {}
    src_count += 1
    if src_count % 2 == 1:
        continue
    for (region, rectangle) in REGIONS.items():
        img = myimgfuncs.load_snip(src, rectangle)
        bounding_box = myimgfuncs.find_bounding_box(img)
        img = myimgfuncs.snip_image(img, bounding_box)
        clean_desperate(img, region)
    """
    shortlist = {}
    for c in desperate:
        res = desperate[c]
        if not res["service_no"].startswith("745394"):
            continue
        if not len(res["surname"].strip()) == 6:
            continue
        if not "Battalion" in res["unit"]:
            continue
        shortlist[c] = res
    pprint(shortlist)
    """
        #img = myimgfuncs.clean(img)
        #img = myimgfuncs.upscale(img)
        #region_filename = OUTPUT_FOLDER + region + ".png"
        #imwrite(region_filename, img)
        #print(myocrfuncs.read_text(img))
    pprint(desperate)
    if src_count > 6:
        print(src_count)
        break