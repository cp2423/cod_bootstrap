import pytesseract
from numpy import ndarray

CAPITALS = "-c tessedit_char_whitelist=" + "".join([chr(i) for i in range(65, 91)])
DIGITS = "-c tessedit_char_whitelist=" + "".join([str(i) for i in range(0, 10)])


def read_text(img: ndarray, options) -> str:
    #img_rgb = cvtColor(img, COLOR_BGR2RGB)
    #return pytesseract.image_to_string(img_rgb)
    return pytesseract.image_to_string(img, config= "--psm 7 " + options)