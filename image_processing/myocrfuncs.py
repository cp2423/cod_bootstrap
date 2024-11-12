from dataclasses import dataclass
from typing import List
import cv2
import myimgfuncs
from myimgfuncs import Rectangle
import pytesseract
from numpy import ndarray

# tesseract options
CAPITALS = "-c tessedit_char_whitelist=" + "".join([chr(i) for i in range(65, 91)])
DIGITS = "-c tessedit_char_whitelist=" + "".join([str(i) for i in range(0, 10)])
# Page Segmentation Mode 7 = "Treat the image as a single text line."
PSM_MODE = "--psm 7"

@dataclass
class Region:
    id: str
    rect: Rectangle
    tesseract_options: str = ""


@dataclass
class ImageObject:
    region: Region
    img: ndarray
    char_boxes: List[Rectangle] = None
    expected_text: str = None


SLICE_1_Y1 = 30   # was 30
SLICE_1_Y2 = 78  # was 65

REGIONS = [
    # NB Rectangle is y1, y2, x1, x2
    Region(
        id="service_no",
        rect=Rectangle(SLICE_1_Y1, SLICE_1_Y2, 190, 350),
        tesseract_options=DIGITS
        ),
    Region(
        id="surname",
        rect=Rectangle(SLICE_1_Y1, SLICE_1_Y2, 600, 850),
        tesseract_options=CAPITALS
        ),
    Region(
        id="forenames",
        rect=Rectangle(SLICE_1_Y1, SLICE_1_Y2, 865, 1150)
        )
]


# All the images are the same width (1200) so this is the only test required
def is_normal_height(img: ndarray) -> bool:
    # these values were found empirically
    return img.shape[0] >= 615 and img.shape[0] <= 619


def read_text(img: ndarray, options) -> str:
    return pytesseract.image_to_string(img, config=f"{PSM_MODE} {options}")


def get_character_boxes(img: ndarray) -> list[Rectangle]:
    cnts = myimgfuncs.find_contours(img)
    rects = []

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        rect = Rectangle(y, y+h, x, x+w)
        rects.append(rect)

    return sorted(rects)


def get_row_objects(binary_img: ndarray):
    contours = myimgfuncs.find_contours(binary_img)
    rows = {}
    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        y_mid = (y+h) / 2
        print(h)
        myimgfuncs.show_img(myimgfuncs.snip_image(binary_img, Rectangle(y, y+h, x, x+w)))
        for row in rows:
            if y_mid > row[0] and y_mid < row[1]:
                rows[row].append(c)
                break
        else:
            row = (y, y+h)
            rows[row] = [c]

    for contours in rows.values():
        if len(contours) >= 3:
            objects = []
            for c in contours:
                ox, oy, ow, oh = cv2.boundingRect(c)
                obj = myimgfuncs.snip_image(binary_img, Rectangle(oy, oy+oh, ox, ox+ow))
                objects.append(obj)

            return objects


KERNEL = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))      # was 9,3
BIG_KERNEL = cv2.getStructuringElement(cv2.MORPH_RECT, (15,9)) # was 15,9

# pre-process each image to find the ROI from the top of the table
def get_top_objects(top_row: ndarray) -> list[ImageObject]:
    top_row = myimgfuncs.resize(top_row, scale_factor=4)
    #gray = cv2.cvtColor(top_row, cv2.COLOR_BGR2GRAY)
    gray = top_row[:,:,2]
    thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)[1]
    myimgfuncs.show_img(thresh)
    #morph = cv2.erode(thresh, KERNEL, iterations=2)
    #myimgfuncs.show_img(morph)
    closure = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, BIG_KERNEL, iterations=5)
    myimgfuncs.show_img(closure)
    row_objects = get_row_objects(closure)
    for obj in row_objects:
        myimgfuncs.show_img(obj)