import cv2
from imgtypes import Img, Rect
from upscaler.edsr_model import SuperRes

MIN_CONTOUR_SIZE = 0  # was 3

upscaler = SuperRes()


def snip_image(img: Img, r: Rect):
    return img[r.y1:r.y2, r.x1:r.x2]



def snip_image(img: Img, x, y, w, h):
    x2 = x+w
    y2 = y+h
    return img[y:y2, x:x2]


# Load image
def load_snip(filepath: str, r: Rect) -> Img:
    # TODO consider if normalization and/or standardization would help?
    # (apparently might help model learn, more research needed)
    img = cv2.imread(filepath)
    return snip_image(img, r)


# Make grayscale, Otsu's threshold
def get_binary_image(img: Img) -> Img:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    return thresh


def denoise(img: Img) -> Img:
    # using recommended values from https://docs.opencv.org/3.4/d5/d69/tutorial_py_non_local_means.html
    return cv2.fastNlMeansDenoising(img, 10, 10, 7, 21)


def dilate(img: Img) -> Img:
    return cv2.dilate(img, None)


def resize(img:Img, scale_factor=2):
    size = (img.shape[1] * scale_factor, img.shape[0] * scale_factor)
    return cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)


def clean(img:Img) -> Img:
    size = (img.shape[1] * 4, img.shape[0] * 4)
    img = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
    img = denoise(img)
    img = dilate(img)
    return img


# original source: https://stackoverflow.com/questions/21104664/extract-all-bounding-boxes-using-opencv-python
def find_contours(binary_img: Img):
     # findContours requires binary image
    #thresh = get_binary_image(img)
    cnts = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    return cnts


# Find all text in area using contours, obtain bounding box
def find_bounding_box(img: Img, show=False) -> Rect:
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

    return Rect(min_y, max_h, min_x, max_w)


def upscale(img: Img) -> Img:
    return upscaler.upscale(img)


def show_img(img: Img, title="image") -> None:
    cv2.imshow(str(title), img)
    cv2.waitKey()