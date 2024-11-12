# implement  https://pyimagesearch.com/2021/12/01/ocr-passports-with-opencv-and-tesseract/

import numpy as np
import pytesseract
import os
import operator
import cv2
from matplotlib import pyplot as plt


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

    # find contours in a row, scanning from top to bottom
    # remove contours before the margin or touching the top (damage)
    filtered_rects = [r for r in rects if r[0] > margin and r[1] > 0]
    # take out small contours
    large_rects = [r for r in filtered_rects if r[2] > 5 and r[3] > 5]

    top_to_bottom_iter = iter(sorted(large_rects, key=operator.itemgetter(1)))

    rows = []
    first_rect = next(top_to_bottom_iter)
    row = [first_rect]

    for rect in top_to_bottom_iter:
        y_mid = first_rect[1] + (first_rect[3] / 2)
        x,y,w,h = rect

        if y < y_mid and (y+h) > y_mid:
            # same row
            row.append(rect)
        else:
            # sort rects in row left to right (x value)
            row.sort(key=operator.itemgetter(0))
            rows.append(row)
            row = [rect]
            first_rect = rect

    DIGITS = "-c tessedit_char_whitelist=" + "".join([str(i) for i in range(0, 10)])

    result = {}

    service_no_rect = rows[1][0]
    print(service_no_rect)
    sx, sy, sw, sh = service_no_rect
    # add 2px padding
    service_no_img = image[sy-2:sy+sh+2, sx:sx+sw]
    plt.imshow(service_no_img)
    service_no_text = pytesseract.image_to_string(service_no_img, config=f"--psm 8 {DIGITS}")
    if service_no_text != "":
        result["service_no"] = {
            "img": service_no_img,
            "text": service_no_text
        }

    return(service_no_img, service_no_text)


FOLDER = "/Users/chris/Dev/cod_records/aws/extracted/31829_B016711/"
IMAGES = [fp for fp in os.scandir(FOLDER) if fp.name.endswith(".jpg")]

for fp in IMAGES:
    fileno = fp.name[-5]
    if int(fileno) % 2 == 1:
        continue
    img, text = process(fp)
    print(text)
    cv2.destroyAllWindows()
    cv2.imshow(text, img)
    cv2.waitKey()