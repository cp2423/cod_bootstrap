import cv2
import os
import myimgfuncs
from numpy import argsort, ndarray

def get_top_row(img: ndarray) -> ndarray:
    slice_red = img[30:75,:,2]
    bigger = myimgfuncs.resize(slice_red, 4)
    thresh = cv2.threshold(bigger, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,5))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
    return morph


def get_chars(img: ndarray):
    MIN_DIM = 10
    MAX_DIM = 90
    words = []
    word = []
    prev_x = 0

    connectivity = 8  # square, not diagonal. or something...
    count, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity)

    # need the components to be sorted in order they appear left to right (numpy sort, not python)
    stats = stats[stats[:, cv2.CC_STAT_LEFT].argsort()]


    # skip first component which is apparently always the background
    for i in range(1, count):
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        w_test = w > MIN_DIM and w < MAX_DIM
        h_test = h > MIN_DIM and h < MAX_DIM
        if w_test and h_test:
            char = myimgfuncs.snip_image(img, x, y, w, h)
            myimgfuncs.show_img(char)
            if x < prev_x + MAX_DIM:
                # char is nearby, so same word
                word.append(char)
            else:
                # store previous word, make new one
                words.append(word)
                word = [char]

    return words


IMAGE_PARENT_FOLDER = "/Users/chris/Dev/cod_records/aws/extracted/"
IMAGE_TEST_FOLDER = IMAGE_PARENT_FOLDER + "31829_B016683/"

for p in os.scandir(IMAGE_TEST_FOLDER):
    print(p)
    if not p.name.endswith(".jpg"):
        print("... is not an image file")
        continue
    img = cv2.imread(p)
    top_row_img = get_top_row(img)
    myimgfuncs.show_img(top_row_img)
    words = get_chars(top_row_img)
    break