# implement  https://pyimagesearch.com/2021/12/01/ocr-passports-with-opencv-and-tesseract/

import numpy as np
import pytesseract
import os
import operator
import cv2
from matplotlib import pyplot as plt


def is_in_range(dim, range_tuple):
    return dim >= range_tuple[0] and dim <= range_tuple[1]


def is_minimum(dim):
    return dim >= 6


def is_candidate(rect):
    x_range = (180, 250)
    y_range = (35, 55)

    tests = [
        is_in_range(rect[0], x_range),
        is_in_range(rect[1], y_range),
        is_minimum(rect[2]),
        is_minimum(rect[3])
    ]

    return all(tests)


def get_service_no_candidates(rects):
    return [r for r in rects if is_candidate(r)]


def process(fp):

    # load the input image, convert it to grayscale, and grab its
    # dimensions
    bgr = cv2.imread(fp)
    # tesseract expects RBG !!
    image = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # initialize a rectangular and square structuring kernel
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (19, 7))

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

    # use the makers mark on the form to chop off the left margin, it's in the middle of y
    img_y_mid = image.shape[0] / 2

    for x,y,w,h in sorted(rects, key=lambda r: r[0]):
        if w > 20 and h > 40:
            if y < img_y_mid and (y+h) > img_y_mid:
                margin = x+w
                break

    DIGITS = "-c tessedit_char_whitelist=" + "".join([str(i) for i in range(0, 10)])

    service_no_candidates = get_service_no_candidates(rects)
    if len(service_no_candidates) == 0:
        print("No candidate service no found")
        return

    if len(service_no_candidates) > 1:
        print("Multiple service no candidates found")

    for i, candidate in enumerate(service_no_candidates):
        print(candidate)
        sx, sy, sw, sh = candidate
        # add 2px padding
        service_no_img = image[sy-2:sy+sh+2, sx:sx+sw]
        service_no_text = pytesseract.image_to_string(service_no_img, config=f"--psm 8 {DIGITS}")
        title = f"{i+1} of {len(service_no_candidates)}  {service_no_text}"
        cv2.imshow(title, service_no_img)
        cv2.waitKey()


FOLDER = "/Users/chris/Dev/cod_records/aws/extracted/31829_B016711/"
IMAGES = [fp for fp in os.scandir(FOLDER) if fp.name.endswith(".jpg")]

for fp in IMAGES:
    fileno = fp.name[-5]
    if int(fileno) % 2 == 1:
        continue
    process(fp)
    cv2.destroyAllWindows()