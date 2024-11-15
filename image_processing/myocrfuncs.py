import cv2
import myimgfuncs
import pytesseract
import numpy as np

from imgtypes import Img, Rect


MIN_NORM_H = 615
MAX_NORM_H = 619
NORM_W = 1200

# tesseract options
CAPITALS = "-c tessedit_char_whitelist=" + "".join([chr(i) for i in range(65, 91)])
DIGITS = "-c tessedit_char_whitelist=" + "".join([str(i) for i in range(0, 10)])
# WAS Page Segmentation Mode 7 = "Treat the image as a single text line."
#PSM_MODE = "--psm 7"
# NOW PSM 8 = Single word
PSM_MODE = "--psm 8"


# All the images are the same width (1200) so this is the only test required
def is_normal_height(img: Img) -> bool:
    # these values were found empirically
    return img.shape[0] >= MIN_NORM_H and img.shape[0] <= MAX_NORM_H


def get_snipped(img: Img, rect: Rect, padding: int):
    x,y,w,h = rect
    x0 = x #- padding
    x1 = x + w #+ padding
    y0 = y - padding
    y1 = y + h + padding

    return img[y0:y1, x0:x1]


def read_text(img: Img, options="") -> str:
    if img is None:
        return ""
    else:
        text = pytesseract.image_to_string(img, config=f"{PSM_MODE} {options}")
        # remove any trailing whitespace
        text = text.strip()
        # remonve any full stop
        text = text.strip('.')

        return text


def get_rgb_img(filepath: str) -> Img:
    bgr = cv2.imread(filepath)
    img = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    if not is_normal_height(img):
        # rescale to "normal" height, maintaining aspect ratio
        print(f"{filepath} is not normal height, currently {img.shape}, resizing")
        scale = MAX_NORM_H / img.shape[0]
        new_w = int(NORM_W * scale)
        img = cv2.resize(img, (new_w, MAX_NORM_H), interpolation=cv2.INTER_LINEAR)

    return img


def get_rects(img: Img) -> list[Rect]:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # initialize a rectangular and square structuring kernel
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 7))

    # smooth the image using a 3x3 Gaussian blur and then apply a
    # blackhat morpholigical operator to find dark regions on a light
    # background
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)

    # compute the Scharr gradient of the blackhat image and scale the
    # result into the range [0, 255]
    grad = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad = np.absolute(grad)
    (minVal, maxVal) = (np.min(grad), np.max(grad))
    grad = (grad - minVal) / (maxVal - minVal)
    grad = (grad * 255).astype("uint8")

    # apply a closing operation using the rectangular kernel to close
    # gaps in between letters -- then apply Otsu's thresholding method
    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(grad, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    rects = [cv2.boundingRect(c) for c in cnts]

    return rects


def is_in_range(dim: int, range_tuple: tuple[int]) -> bool:
    return dim >= range_tuple[0] and dim <= range_tuple[1]


def is_minimum(dim: int) -> bool:
    return dim >= 6

