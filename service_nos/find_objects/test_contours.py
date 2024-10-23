# find objects using contours
# https://stackoverflow.com/questions/21104664/extract-all-bounding-boxes-using-opencv-python

import cv2
import pandas as pd

GEORGE = "/Users/chris/Dev/cod_records/george circumstance of death.jpg"
#df = pd.DataFrame(columns=["x","y","w","h"])

# crop
# l-r 190 - 300
# t-b 30 - 65

# Load image, grayscale, Otsu's threshold
image = cv2.imread(GEORGE)[30:65, 190:300]
original = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find contours, obtain bounding box, extract and save ROI
min_x = min_y = 300 - 190
max_w = max_h = 0
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    if w < 5 or h < 5:
        continue
    if x < min_x: min_x = x
    if y < min_y: min_y = y
    if x + w > max_w: max_w = x + w
    if y + h > max_h: max_h = y + h
    #cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)

cv2.rectangle(image, (min_x, min_y), (max_w, max_h), (36,12,255), 2)
ROI = original[min_y:max_h, min_x:max_w]
cv2.imwrite('ROI.png', ROI)

data = [(cv2.boundingRect(c)) for c in cnts]
df = pd.DataFrame(data, columns=["x","y","w","h"])

#print(df.w.value_counts())

cv2.imshow('image', image)
cv2.waitKey()