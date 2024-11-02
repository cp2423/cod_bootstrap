import cv2
from dataclasses import dataclass
from numpy import ndarray
from upscaler.edsr_model import SuperRes

MIN_CONTOUR_SIZE = 0  # was 3

upscaler = SuperRes()

@dataclass(order=True)
class Rectangle:
    y1: int
    y2: int
    x1: int
    x2: int

    def __post_init__(self):
        self.sort_index = self.x1


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
    size = (img.shape[1] * 4, img.shape[0] * 4)
    img = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
    img = denoise(img)
    img = dilate(img)
    return img


# original source: https://stackoverflow.com/questions/21104664/extract-all-bounding-boxes-using-opencv-python
def find_contours(img: ndarray):
     # findContours requires binary image
    thresh = get_binary_image(img)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    return cnts


# Find all text in area using contours, obtain bounding box
def find_bounding_box(img: ndarray, show=False) -> Rectangle:
    # initalise box to cover whole image
    min_y = img.shape[0]  # 0 => rows
    min_x = img.shape[1]  # 1 => cols
    max_w = max_h = 0

    # find all contours
    cnts = find_contours(img)

    # iteratively narrow box down to region of image
    print("Countours found:", len(cnts))
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        # throw out small boxes
        if w < MIN_CONTOUR_SIZE or h < MIN_CONTOUR_SIZE:
            continue
        # throw out rectangular boxes
        ratio = w / h
        print(ratio)
        if x < min_x: min_x = x
        if y < min_y: min_y = y
        if x + w > max_w: max_w = x + w
        if y + h > max_h: max_h = y + h

        if show:
            cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 1)

    if show:
        show_img(img, len(cnts))

    return Rectangle(min_y, max_h, min_x, max_w)


def upscale(img: ndarray) -> ndarray:
    return upscaler.upscale(img)


def show_img(img: ndarray, title="image") -> None:
    cv2.imshow(str(title), img)
    cv2.waitKey()