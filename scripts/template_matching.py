from __future__ import print_function
import sys
import cv2 as cv
import os

## [global_variables]
use_mask = False
img = None
templ = None
mask = None
image_window = "Source Image"
result_window = "Result window"

match_method = 0
max_Trackbar = 5
## [global_variables]

def main(args):
    ## [load_image]
    global img
    global templ
    img = cv.imread(args[0], cv.IMREAD_GRAYSCALE)
    templ = cv.imread(args[1], cv.IMREAD_GRAYSCALE)

    if (len(sys.argv) > 3):
        global use_mask
        use_mask = True
        global mask
        mask = cv.imread( sys.argv[3], cv.IMREAD_COLOR )

    if ((img is None) or (templ is None) or (use_mask and (mask is None))):
        print('Can\'t read one of the images')
        return -1
    ## [load_image]

    ## [create_windows]
    cv.namedWindow( image_window, cv.WINDOW_AUTOSIZE )
    ## [create_windows]

    MatchingMethod(cv.TM_SQDIFF_NORMED)

    ## [wait_key]
    cv.waitKey(0)
    return 0
    ## [wait_key]

def MatchingMethod(param):

    global match_method
    match_method = param

    ## [copy_source]
    img_display = img.copy()
    ## [copy_source]
    ## [match_template]
    method_accepts_mask = (cv.TM_SQDIFF == match_method or match_method == cv.TM_CCORR_NORMED)
    if (use_mask and method_accepts_mask):
        result = cv.matchTemplate(img, templ, match_method, None, mask)
    else:
        result = cv.matchTemplate(img, templ, match_method)
    ## [match_template]

    ## [best_match]
    _minVal, _maxVal, minLoc, maxLoc = cv.minMaxLoc(result, None)
    ## [best_match]

    ## [match_loc]
    if (match_method == cv.TM_SQDIFF or match_method == cv.TM_SQDIFF_NORMED):
        matchLoc = minLoc
    else:
        matchLoc = maxLoc
    ## [match_loc]

    ## [imshow]
    print(matchLoc)
    print(matchLoc[0], templ.shape[0], matchLoc[1], templ.shape[1])
    print(matchLoc[0] + templ.shape[1], matchLoc[1] + templ.shape[0])
    cv.rectangle(img_display, matchLoc, (matchLoc[0] + templ.shape[1], matchLoc[1] + templ.shape[0]), (0,0,0), 2, 8, 0 )
    cv.imshow(image_window, img_display)
    cv.waitKey()
    ## [imshow]
    pass

if __name__ == "__main__":
    args = [
        #"/Users/chris/Dev/cod_records/aws/extracted/31829_B016711/31829_B016711-00000.jpg",
        "/Users/chris/Dev/cod_records/george circumstance of death.jpg",
        "/Users/chris/Dev/cod_records/cod_bootstrap/templates/date_of_casualty.png"
    ]
    #main(sys.argv[1:])
    for fp in os.scandir("/Users/chris/Dev/cod_records/aws/extracted/31829_B016711/"):
        args[0] = fp
        main(args)