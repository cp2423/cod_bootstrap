import cv2
from dataclasses import dataclass
from numpy import ndarray
from upscaler.edsr_model import SuperRes

MIN_CONTOUR_SIZE = 3

upscaler = SuperRes()

@dataclass
class Rectangle:
    y1: int
    y2: int
    x1: int
    x2: int


def snip_image(img: ndarray, r: Rectangle):
    return img[r.y1:r.y2, r.x1:r.x2]


# Load image
def load_snip(filepath: str, r: Rectangle) -> ndarray:
    # TODO consider if normalization and/or standardization would help?
    # (apparently might help model learn, more research needed)
    img = cv2.imread(filepath)
    return snip_image(img, r)


# Make grayscale, Otsu's threshold
def get_binary_image(img: ndarray) -> ndarray:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    return thresh


def denoise(img: ndarray) -> ndarray:
    # using recommended values from https://docs.opencv.org/3.4/d5/d69/tutorial_py_non_local_means.html
    return cv2.fastNlMeansDenoising(img, 10, 10, 7, 21)


def dilate(img: ndarray) -> ndarray:
    return cv2.dilate(img, None)

def clean(img:ndarray) -> ndarray:
    size = (img.shape[1] * 2, img.shape[0] * 2)
    img = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
    img = get_binary_image(img)
    #img = denoise(img)
    img = dilate(img)
    return img


# Find contours, obtain bounding box
def find_bounding_box(img: ndarray) -> Rectangle:
    # findContours requires binary image
    thresh = get_binary_image(img)

    # initalise box to cover whole image
    min_y = img.shape[0]  # 0 => rows
    min_x = img.shape[1]  # 1 => cols
    max_w = max_h = 0

    # find all contours
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    # iteratively narrow box down to region of image
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w < MIN_CONTOUR_SIZE or h < MIN_CONTOUR_SIZE:
            continue
        if x < min_x: min_x = x
        if y < min_y: min_y = y
        if x + w > max_w: max_w = x + w
        if y + h > max_h: max_h = y + h

    return Rectangle(min_y, max_h, min_x, max_w)


def upscale(img: ndarray) -> ndarray:
    return upscaler.upscale(img)


def show(img: ndarray) -> None:
    cv2.imshow("image", img)
    cv2.waitKey()