import cv2
import myimgfuncs
from myimgfuncs import Rectangle
import pytesseract
from numpy import ndarray

CAPITALS = "-c tessedit_char_whitelist=" + "".join([chr(i) for i in range(65, 91)])
DIGITS = "-c tessedit_char_whitelist=" + "".join([str(i) for i in range(0, 10)])


def read_text(img: ndarray, options) -> str:
    return pytesseract.image_to_string(img, config= "--psm 7 " + options)


def find_character_boxes(img: ndarray) -> list[Rectangle]:
    cnts = myimgfuncs.find_contours(img)

    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)