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